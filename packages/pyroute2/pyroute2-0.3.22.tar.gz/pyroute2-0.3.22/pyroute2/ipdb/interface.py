import time
import errno
import socket
import threading
import traceback
from pyroute2 import config
from pyroute2.common import basestring
from pyroute2.common import reduce
from pyroute2.common import dqn2int
from pyroute2.netlink.exceptions import NetlinkError
from pyroute2.netlink.rtnl.req import IPLinkRequest
from pyroute2.netlink.rtnl.ifinfmsg import IFF_MASK
from pyroute2.netlink.rtnl.ifinfmsg import ifinfmsg
from pyroute2.ipdb.transactional import Transactional
from pyroute2.ipdb.transactional import with_transaction
from pyroute2.ipdb.transactional import SYNC_TIMEOUT
from pyroute2.ipdb.linkedset import LinkedSet
from pyroute2.ipdb.linkedset import IPaddrSet
from pyroute2.ipdb.exceptions import CreateException
from pyroute2.ipdb.exceptions import CommitException
from pyroute2.ipdb.exceptions import PartialCommitException


def _get_data_fields():
    ret = []
    for data in ('bridge_data',
                 'bond_data',
                 'tuntap_data',
                 'vxlan_data',
                 'gre_data',
                 'macvlan_data',
                 'macvtap_data',
                 'ipvlan_data',
                 'vrf_data'):
        msg = getattr(ifinfmsg.ifinfo, data)
        ret += [msg.nla2name(i[0]) for i in msg.nla_map]
    return ret


class Interface(Transactional):
    '''
    Objects of this class represent network interface and
    all related objects:
    * addresses
    * (todo) neighbours
    * (todo) routes

    Interfaces provide transactional model and can act as
    context managers. Any attribute change implicitly
    starts a transaction. The transaction can be managed
    with three methods:
    * review() -- review changes
    * rollback() -- drop all the changes
    * commit() -- try to apply changes

    If anything will go wrong during transaction commit,
    it will be rolled back authomatically and an
    exception will be raised. Failed transaction review
    will be attached to the exception.
    '''
    _fields_cmp = {'flags': lambda x, y: x & y & IFF_MASK == y & IFF_MASK}
    _virtual_fields = ['ipdb_scope', 'ipdb_priority']
    _xfields = {'common': [ifinfmsg.nla2name(i[0]) for i
                           in ifinfmsg.nla_map]}
    _xfields['common'].append('index')
    _xfields['common'].append('flags')
    _xfields['common'].append('mask')
    _xfields['common'].append('change')
    _xfields['common'].append('kind')
    _xfields['common'].append('peer')
    _xfields['common'].append('vlan_id')
    _xfields['common'].append('bond_mode')
    _xfields['common'].extend(_get_data_fields())

    _fields = reduce(lambda x, y: x + y, _xfields.values())
    _fields.extend(_virtual_fields)

    def __init__(self, ipdb, mode=None, parent=None, uid=None):
        '''
        Parameters:
        * ipdb -- ipdb() reference
        * mode -- transaction mode
        '''
        Transactional.__init__(self, ipdb, mode)
        self.cleanup = ('header',
                        'linkinfo',
                        'protinfo',
                        'af_spec',
                        'attrs',
                        'event',
                        'map',
                        'stats',
                        'stats64',
                        '__align')
        self.ingress = None
        self.egress = None
        self.nlmsg = None
        self.errors = []
        self.partial = False
        self._exception = None
        self._tb = None
        self._load_event = threading.Event()
        self._linked_sets.add('ipaddr')
        self._linked_sets.add('ports')
        self._linked_sets.add('vlans')
        self._freeze = None
        self._delay_add_port = set()
        self._delay_del_port = set()
        # 8<-----------------------------------
        # local setup: direct state is required
        with self._direct_state:
            for i in ('change', 'mask'):
                del self[i]
            self['ipaddr'] = IPaddrSet()
            self['ports'] = LinkedSet()
            self['vlans'] = LinkedSet()
            self['ipdb_priority'] = 0
        # 8<-----------------------------------

    def __hash__(self):
        return self['index']

    @property
    def if_master(self):
        '''
        [property] Link to the parent interface -- if it exists
        '''
        return self.get('master', None)

    def detach(self):
        self.ipdb.detach(self['ifname'], self['index'], self.nlmsg)
        return self

    def freeze(self):
        dump = self.pick()

        def cb(ipdb, msg, action):
            if msg.get('index', -1) == dump['index']:
                try:
                    # important: that's a rollback, so do not
                    # try to revert changes in the case of failure
                    self.commit(transaction=dump, rollback=True)
                except Exception:
                    pass

        self._freeze = self.ipdb.register_callback(cb)
        return self

    def unfreeze(self):
        self.ipdb.unregister_callback(self._freeze)
        self._freeze = None
        return self

    def load(self, data):
        '''
        Load the data from a dictionary to an existing
        transaction. Requires `commit()` call, or must be
        called from within a `with` statement.

        Sample::

            data = json.loads(...)
            with ipdb.interfaces['dummy1'] as i:
                i.load(data)

        Sample, mode `explicit::

            data = json.loads(...)
            i = ipdb.interfaces['dummy1']
            i.begin()
            i.load(data)
            i.commit()
        '''
        for key in data:
            if key == 'ipaddr':
                for addr in self['ipaddr']:
                    self.del_ip(*addr)
                for addr in data[key]:
                    if isinstance(addr, basestring):
                        addr = (addr, )
                    self.add_ip(*addr)
            elif key == 'ports':
                for port in self['ports']:
                    self.del_port(port)
                for port in data[key]:
                    self.add_port(port)
            elif key == 'vlans':
                for vlan in self['vlans']:
                    self.del_vlan(vlan)
                for vlan in data[key]:
                    self.add_vlan(vlan)
            elif key == 'neighbours':
                # ignore neighbours on load
                pass
            else:
                self[key] = data[key]
        return self

    def make_transaction(self, data):
        '''
        Create a new transaction instance from a dictionary.
        One can apply it the with `commit(transaction=...)`
        call.

        Sample::

            data = json.loads(...)
            t = ipdb.interfaces['dummy1'].make_transaction(data)
            ipdb.interfaces['dummy1'].commit(transaction=t)
        '''
        with self._write_lock:
            template = self.__class__(ipdb=self.ipdb, mode='snapshot')
            template.load_dict(data)
            return template

    def load_dict(self, data):
        '''
        Update the interface info from a dictionary.

        This call always bypasses open transactions, loading
        changes directly into the interface data.
        '''
        with self._direct_state:
            self.load(data)

    def load_netlink(self, dev):
        '''
        Update the interface info from RTM_NEWLINK message.

        This call always bypasses open transactions, loading
        changes directly into the interface data.
        '''
        with self._direct_state:
            if self['ipdb_scope'] == 'locked':
                # do not touch locked interfaces
                return

            if self['ipdb_scope'] in ('shadow', 'create'):
                # ignore non-broadcast messages
                if dev['header']['sequence_number'] != 0:
                    return
                # ignore ghost RTM_NEWLINK messages
                if (config.kernel[0] < 3) and \
                        (not dev.get_attr('IFLA_AF_SPEC')):
                    return
            self['ipdb_scope'] = 'system'
            if self.ipdb.debug:
                self.nlmsg = dev
            for (name, value) in dev.items():
                self[name] = value
            for item in dev['attrs']:
                name, value = item[:2]
                norm = ifinfmsg.nla2name(name)
                self[norm] = value
            # load interface kind
            linkinfo = dev.get_attr('IFLA_LINKINFO')
            if linkinfo is not None:
                kind = linkinfo.get_attr('IFLA_INFO_KIND')
                if kind is not None:
                    self['kind'] = kind
                    if kind == 'vlan':
                        data = linkinfo.get_attr('IFLA_INFO_DATA')
                        self['vlan_id'] = data.get_attr('IFLA_VLAN_ID')
                    if kind in ('vxlan', 'macvlan', 'macvtap',
                                'gre', 'gretap', 'ipvlan'):
                        data = linkinfo.get_attr('IFLA_INFO_DATA')
                        for nla in data.get('attrs', []):
                            norm = ifinfmsg.nla2name(nla[0])
                            self[norm] = nla[1]
            # load vlans
            if dev['family'] == socket.AF_BRIDGE:
                spec = dev.get_attr('IFLA_AF_SPEC')
                if spec is not None:
                    vlans = spec.get_attrs('IFLA_BRIDGE_VLAN_INFO')
                    vmap = {}
                    for vlan in vlans:
                        vmap[vlan['vid']] = vlan
                    vids = set(vmap.keys())
                    # remove vids we do not have anymore
                    for vid in (self['vlans'] - vids):
                        self.del_vlan(vid)
                    for vid in (vids - self['vlans']):
                        self.add_vlan(vmap[vid])
            # the rest is possible only when interface
            # is used in IPDB, not standalone
            if self.ipdb is not None:
                self['ipaddr'] = self.ipdb.ipaddr[self['index']]
                self['neighbours'] = self.ipdb.neighbours[self['index']]
            # finally, cleanup all not needed
            for item in self.cleanup:
                if item in self:
                    del self[item]

            # AF_BRIDGE messages for bridges contain
            # IFLA_MASTER == self.index, we should fix it
            if self.get('master', None) == self['index']:
                self['master'] = None

            self.sync()

    def sync(self):
        self._load_event.set()

    def wait_ip(self, *argv, **kwarg):
        return self['ipaddr'].wait_ip(*argv, **kwarg)

    @with_transaction
    def add_ip(self, ip, mask=None, broadcast=None, anycast=None, scope=None):
        '''
        Add IP address to an interface

        Keyword arguments:

        * mask
        * broadcast
        * anycast
        * scope
        '''
        # split mask
        if mask is None:
            ip, mask = ip.split('/')
            if mask.find('.') > -1:
                mask = dqn2int(mask)
            else:
                mask = int(mask, 0)
        elif isinstance(mask, basestring):
            mask = dqn2int(mask)

        # FIXME: make it more generic
        # skip IPv6 link-local addresses
        if ip[:4] == 'fe80' and mask == 64:
            return self

        # if it is a transaction or an interface update, apply the change
        self['ipaddr'].unlink((ip, mask))
        request = {}
        if broadcast is not None:
            request['broadcast'] = broadcast
        if anycast is not None:
            request['anycast'] = anycast
        if scope is not None:
            request['scope'] = scope
        self['ipaddr'].add((ip, mask), raw=request)

    @with_transaction
    def del_ip(self, ip, mask=None):
        '''
        Delete IP address from an interface
        '''
        if mask is None:
            ip, mask = ip.split('/')
            if mask.find('.') > -1:
                mask = dqn2int(mask)
            else:
                mask = int(mask, 0)
        if (ip, mask) in self['ipaddr']:
            self['ipaddr'].unlink((ip, mask))
            self['ipaddr'].remove((ip, mask))

    @with_transaction
    def add_vlan(self, vlan):
        if isinstance(vlan, dict):
            vid = vlan['vid']
        else:
            vid = vlan
            vlan = {'vid': vlan, 'flags': 0}
        self['vlans'].unlink(vid)
        self['vlans'].add(vid, raw=vlan)

    @with_transaction
    def del_vlan(self, vlan):
        if vlan in self['vlans']:
            self['vlans'].unlink(vlan)
            self['vlans'].remove(vlan)

    @with_transaction
    def add_port(self, port):
        '''
        Add port to a bridge or bonding
        '''
        ifindex = self._resolve_port(port)
        if ifindex is None:
            self._delay_add_port.add(port)
        else:
            self['ports'].unlink(ifindex)
            self['ports'].add(ifindex)

    @with_transaction
    def del_port(self, port):
        '''
        Remove port from a bridge or bonding
        '''
        ifindex = self._resolve_port(port)
        if ifindex is None:
            self._delay_del_port.add(port)
        else:
            self['ports'].unlink(ifindex)
            self['ports'].remove(ifindex)

    def reload(self):
        '''
        Reload interface information
        '''
        countdown = 3
        while countdown:
            links = self.nl.get_links(self['index'])
            if links:
                self.load_netlink(links[0])
                break
            else:
                countdown -= 1
                time.sleep(1)
        return self

    def filter(self, ftype):
        ret = {}
        for key in self:
            if key in self._xfields[ftype]:
                ret[key] = self[key]
        return ret

    def review(self):
        ret = super(Interface, self).review()
        last = self.last()
        if self['ipdb_scope'] == 'create':
            ret['+ipaddr'] = last['ipaddr']
            ret['+ports'] = last['ports']
            ret['+vlans'] = last['vlans']
            del ret['ports']
            del ret['ipaddr']
            del ret['vlans']
        if last._delay_add_port:
            ports = set(['*%s' % x for x in last._delay_add_port])
            if '+ports' in ret:
                ret['+ports'] |= ports
            else:
                ret['+ports'] = ports
        if last._delay_del_port:
            ports = set(['*%s' % x for x in last._delay_del_port])
            if '-ports' in ret:
                ret['-ports'] |= ports
            else:
                ret['-ports'] = ports
        return ret

    def _run(self, cmd, *argv, **kwarg):
        try:
            return cmd(*argv, **kwarg)
        except Exception as error:
            if self.partial:
                self.errors.append(error)
                return []
            raise error

    def _resolve_port(self, port):
        # for now just a stupid resolver, will be
        # improved later with search by mac, etc.
        if isinstance(port, Interface):
            return port['index']
        else:
            return self.ipdb.interfaces.get(port, {}).get('index', None)

    def _commit_add_ip(self, addrs, transaction):
        for i in addrs:
            # Ignore link-local IPv6 addresses
            if i[0][:4] == 'fe80' and i[1] == 64:
                continue
            # Try to fetch additional address attributes
            try:
                kwarg = dict([k for k in transaction.ipaddr[i].items()
                              if k[0] in ('broadcast',
                                          'anycast',
                                          'scope')])
            except KeyError:
                kwarg = None
            # feed the address to the OS
            self.ipdb.update_addr(
                transaction._run(transaction.nl.addr, 'add',
                                 self['index'], i[0], i[1],
                                 **kwarg if kwarg else {}), 'add')

            # 8<--------------------------------------
            # FIXME: kernel bug, sometimes `addr add` for
            # bond interfaces returns success, but does
            # really nothing

            if self['kind'] == 'bond':
                while True:
                    try:
                        # dirtiest hack, but we have to use it here
                        self.nl.addr('add', self['index'], i[0], i[1])
                        time.sleep(0.1)
                    # continue to try to add the address
                    # until the kernel reports `file exists`
                    #
                    # a stupid solution, but must help
                    except NetlinkError as e:
                        if e.code == errno.EEXIST:
                            break
                        else:
                            raise
                    except Exception:
                        raise

    def commit(self, tid=None, transaction=None, rollback=False, newif=False):
        '''
        Commit transaction. In the case of exception all
        changes applied during commit will be reverted.
        '''
        error = None
        added = None
        removed = None
        drop = True
        if tid:
            transaction = self._transactions[tid]
        else:
            if transaction:
                drop = False
            else:
                transaction = self.last()
        if transaction.partial:
            transaction.errors = []

        wd = None
        with self._write_lock:
            # if the interface does not exist, create it first ;)
            if self['ipdb_scope'] != 'system':
                request = IPLinkRequest(self.filter('common'))

                # create watchdog
                wd = self.ipdb.watchdog(ifname=self['ifname'])

                newif = True
                try:
                    # 8<----------------------------------------------------
                    # ACHTUNG: hack for old platforms
                    if request.get('address', None) == '00:00:00:00:00:00':
                        del request['address']
                        del request['broadcast']
                    # 8<----------------------------------------------------
                    try:
                        self.nl.link('add', **request)
                    except NetlinkError as x:
                        # File exists
                        if x.code == errno.EEXIST:
                            # A bit special case, could be one of two cases:
                            #
                            # 1. A race condition between two different IPDB
                            #    processes
                            # 2. An attempt to create dummy0, gre0, bond0 when
                            #    the corrseponding module is not loaded. Being
                            #    loaded, the module creates a default interface
                            #    by itself, causing the request to fail
                            #
                            # The exception in that case can cause the DB
                            # inconsistence, since there can be queued not only
                            # the interface creation, but also IP address
                            # changes etc.
                            #
                            # So we ignore this particular exception and try to
                            # continue, as it is created by us.
                            pass

                        # Operation not supported
                        elif x.code == errno.EOPNOTSUPP and \
                                request.get('index', 0) != 0:
                            # ACHTUNG: hack for old platforms
                            request = IPLinkRequest({'ifname': self['ifname'],
                                                     'kind': self['kind'],
                                                     'index': 0})
                            self.nl.link('add', **request)
                        else:
                            raise
                except Exception as e:
                    # on failure, invalidate the interface and detach it
                    # from the parent
                    # 1. drop the IPRoute() link
                    self.nl = None
                    # 2. clean up ipdb
                    self.detach()
                    # 3. invalidate the interface
                    with self._direct_state:
                        for i in tuple(self.keys()):
                            del self[i]
                    # 4. the rest
                    self._mode = 'invalid'
                    self._exception = e
                    self._tb = traceback.format_exc()
                    # raise the exception
                    if transaction.partial:
                        transaction.errors.append(e)
                        raise PartialCommitException()
                    else:
                        raise

        if wd is not None:
            # Here we come only if the new interface is created
            #
            wd.wait()
            if self['index'] == 0:
                # Only the interface creation time issue on
                # old or compat platforms. The interface index
                # may be not known yet, but we can not continue
                # without it. It will be updated anyway, but
                # it is better to force the lookup.
                #
                ix = self.nl.link_lookup(ifname=self['ifname'])
                if ix:
                    self['index'] = ix[0]
                else:
                    if transaction.partial:
                        transaction.errors.append(CreateException())
                        raise PartialCommitException()
                    else:
                        raise CreateException()
            # Re-populate transaction.ipaddr to have a proper IP target
            #
            # The reason behind the code is that a new interface in the
            # "up" state will have automatic IPv6 addresses, that aren't
            # reflected in the transaction. This may cause a false IP
            # target mismatch and a commit failure.
            #
            # To avoid that, collect automatic addresses to the
            # transaction manually, since it is not yet properly linked.
            #
            map(transaction['ipaddr'].add, self.ipdb.ipaddr[self['index']])

        # now we have our index and IP set and all other stuff
        snapshot = self.pick()

        # resolve all delayed ports
        def resolve_ports(transaction, ports, callback, self, drop):
            def error(x):
                return KeyError('can not resolve port %s' % x)
            for port in tuple(ports):
                ifindex = self._resolve_port(port)
                if ifindex is None:
                    if transaction.partial:
                        transaction.errors.append(error(port))
                    else:
                        if drop:
                            self.drop(transaction)
                        raise error(port)
                else:
                    ports.remove(port)
                    callback(ifindex, direct=True)
        resolve_ports(transaction,
                      transaction._delay_add_port,
                      transaction.add_port,
                      self, drop)
        resolve_ports(transaction,
                      transaction._delay_del_port,
                      transaction.del_port,
                      self, drop)

        try:
            removed = snapshot - transaction
            added = transaction - snapshot

            run = transaction._run
            nl = transaction.nl

            # 8<---------------------------------------------
            # Port vlans
            self['vlans'].set_target(transaction['vlans'])
            for i in removed['vlans']:
                # remove vlan from the port
                run(nl.vlan_filter, 'del',
                    index=self['index'],
                    vlan_info=self['vlans'][i])

            for i in added['vlans']:
                # add vlan to the port
                run(nl.vlan_filter, 'add',
                    index=self['index'],
                    vlan_info=transaction['vlans'][i])

            if (not transaction.partial) and \
                    (removed['vlans'] or added['vlans']):
                self['vlans'].target.wait(SYNC_TIMEOUT)
                if not self['vlans'].target.is_set():
                    raise CommitException('vlans target is not set')

            # 8<---------------------------------------------
            # Ports
            self['ports'].set_target(transaction['ports'])
            for i in removed['ports']:
                # detach port
                if i in self.ipdb.interfaces:
                    port = self.ipdb.interfaces[i]
                    port.set_target('master', None)
                    port.mirror_target('master', 'link')
                    run(nl.link, 'set',
                        index=port['index'],
                        master=0)
                else:
                    transaction.errors.append(KeyError(i))

            for i in added['ports']:
                # attach port
                if i in self.ipdb.interfaces:
                    port = self.ipdb.interfaces[i]
                    port.set_target('master', self['index'])
                    port.mirror_target('master', 'link')
                    run(nl.link, 'set',
                        index=port['index'],
                        master=self['index'])
                else:
                    transaction.errors.append(KeyError(i))

            if (not transaction.partial) and \
                    (removed['ports'] or added['ports']):
                for link in self.nl.get_links(
                        *(removed['ports'] | added['ports'])):
                    self.ipdb.device_put(link)
                self['ports'].target.wait(SYNC_TIMEOUT)
                if not self['ports'].target.is_set():
                    raise CommitException('ports target is not set')

                # wait for proper targets on ports
                for i in list(added['ports']) + list(removed['ports']):
                    port = self.ipdb.interfaces[i]
                    target = port._local_targets['master']
                    target.wait(SYNC_TIMEOUT)
                    del port._local_targets['master']
                    del port._local_targets['link']
                    if not target.is_set():
                        raise CommitException('master target failed')
                    if i in added['ports']:
                        if port.if_master != self['index']:
                            raise CommitException('master set failed')
                    else:
                        if port.if_master == self['index']:
                            raise CommitException('master unset failed')

            # 8<---------------------------------------------
            # Interface changes
            request = IPLinkRequest()
            for key in added:
                if (key in self._xfields['common']) and \
                        (key != 'kind'):
                    request[key] = added[key]
            request['index'] = self['index']

            # apply changes only if there is something to apply
            if any([request[item] is not None for item in request
                    if item != 'index']):
                if request.get('address', None) == '00:00:00:00:00:00':
                    request.pop('address')
                    request.pop('broadcast', None)
                run(nl.link, 'set', **request)
                # hardcoded pause -- if the interface was moved
                # across network namespaces
                if not transaction.partial and 'net_ns_fd' in request:
                    while True:
                        # wait until the interface will disappear
                        # from the main network namespace
                        try:
                            for link in self.nl.get_links(self['index']):
                                self.ipdb.device_put(link)
                        except NetlinkError as e:
                            if e.code == errno.ENODEV:
                                break
                            raise
                        except Exception:
                            raise
                    time.sleep(0.1)

            # 8<---------------------------------------------
            # IP address changes
            self['ipaddr'].set_target(transaction['ipaddr'])

            # The promote_secondaries sysctl causes the kernel
            # to add secondary addresses back after the primary
            # address is removed.
            #
            # The library can not tell this from the result of
            # an external program.
            #
            # One simple way to work that around is to remove
            # secondaries first.
            rip = sorted(removed['ipaddr'],
                         key=lambda x: self['ipaddr'][x]['flags'],
                         reverse=True)
            # 8<--------------------------------------
            for i in rip:
                # Ignore link-local IPv6 addresses
                if i[0][:4] == 'fe80' and i[1] == 64:
                    continue
                # When you remove a primary IP addr, all subnetwork
                # can be removed. In this case you will fail, but
                # it is OK, no need to roll back
                try:
                    self.ipdb.update_addr(
                        run(nl.addr, 'delete', self['index'], i[0], i[1]),
                        'remove')
                except NetlinkError as x:
                    # bypass only errno 99, 'Cannot assign address'
                    if x.code != errno.EADDRNOTAVAIL:
                        raise
                except socket.error as x:
                    # bypass illegal IP requests
                    if isinstance(x.args[0], basestring) and \
                            x.args[0].startswith('illegal IP'):
                        continue
                    raise

            # 8<--------------------------------------
            target = added['ipaddr']
            for _ in range(3):  # just to be sure
                self._commit_add_ip(target, transaction)
                if transaction.partial:
                    break
                for _ in range(3):
                    # sometimes addr("dump") after addr("add")
                    # fails with EBUSY, so try again
                    try:
                        real = set([(m.get_attr('IFA_ADDRESS'),
                                     m.get('prefixlen')) for m
                                    in self.nl.get_addr(index=self.index)])
                        break
                    except NetlinkError as x:
                        if x.code == errno.EBUSY:
                            time.sleep(0.5)
                        else:
                            raise
                if real >= set(transaction['ipaddr']):
                    break
                else:
                    target = set(transaction['ipaddr']) - real
            else:
                raise CommitException('ipaddr setup error')

            # 8<--------------------------------------
            if (not transaction.partial) and \
                    (removed['ipaddr'] or added['ipaddr']):
                # 8<--------------------------------------
                # bond and bridge interfaces do not send
                # IPv6 address updates, when are down
                #
                # beside of that, bridge interfaces are
                # down by default, so they never send
                # address updates from beginning
                #
                # so if we need, force address load
                #
                # FIXME: probably, we should handle other
                # types as well
                if self['kind'] in ('bond', 'bridge', 'veth'):
                    self.ipdb.update_addr(self.nl.get_addr(), 'add')
                # 8<--------------------------------------
                self['ipaddr'].target.wait(SYNC_TIMEOUT)
                if not self['ipaddr'].target.is_set():
                    raise CommitException('ipaddr target is not set')

            # 8<---------------------------------------------
            # Iterate callback chain
            for ch in self._commit_hooks:
                # An exception will rollback the transaction
                ch(self.dump(), snapshot.dump(), transaction.dump())

            # 8<---------------------------------------------
            # reload interface to hit targets
            if not transaction.partial:
                if transaction._targets:
                    try:
                        self.reload()
                    except NetlinkError as e:
                        if e.code == errno.ENODEV:  # No such device
                            if ('net_ns_fd' in added) or \
                                    ('net_ns_pid' in added):
                                # it means, that the device was moved
                                # to another netns; just give up
                                if drop:
                                    self.drop(transaction)
                                return self
                # wait for targets
                transaction._wait_all_targets()

            # 8<---------------------------------------------
            # Interface removal
            if (added.get('ipdb_scope') in ('shadow', 'remove')) or\
                    ((added.get('ipdb_scope') == 'create') and rollback):
                wd = self.ipdb.watchdog(action='RTM_DELLINK',
                                        ifname=self['ifname'])
                if added.get('ipdb_scope') in ('shadow', 'create'):
                    self.set_item('ipdb_scope', 'locked')
                self.nl.link('delete', **self)
                wd.wait()
                if added.get('ipdb_scope') == 'shadow':
                    self.set_item('ipdb_scope', 'shadow')
                if added['ipdb_scope'] == 'create':
                    self.load_dict(transaction)
                if drop:
                    self.drop(transaction)
                return self
            # 8<---------------------------------------------

        except Exception as e:
            error = e
            # something went wrong: roll the transaction back
            if not rollback:
                try:
                    self.commit(transaction=snapshot,
                                rollback=True,
                                newif=newif)
                except Exception as i_e:
                    error = RuntimeError()
                    error.cause = i_e
            else:
                # reload all the database -- it can take a long time,
                # but it is required since we have no idea, what is
                # the result of the failure
                links = self.nl.get_links()
                for link in links:
                    self.ipdb.device_put(link, skip_slaves=True)
                for link in links:
                    self.ipdb.update_slaves(link)
                links = self.nl.get_vlans()
                for link in links:
                    self.ipdb.update_dev(link)
                self.ipdb.update_addr(self.nl.get_addr())

            error.traceback = traceback.format_exc()
            for key in ('ipaddr', 'ports', 'vlans'):
                self[key].clear_target()

        # raise partial commit exceptions
        if transaction.partial and transaction.errors:
            error = PartialCommitException('partial commit error')

        # if it is not a rollback turn
        if drop and not rollback:
            # drop last transaction in any case
            self.drop(transaction)

        # raise exception for failed transaction
        if error is not None:
            error.transaction = transaction
            raise error

        time.sleep(config.commit_barrier)

        # drop all collected errors, if any
        self.errors = []
        return self

    def up(self):
        '''
        Shortcut: change the interface state to 'up'.
        '''
        if self['flags'] is None:
            self['flags'] = 1
        else:
            self['flags'] |= 1
        return self

    def down(self):
        '''
        Shortcut: change the interface state to 'down'.
        '''
        if self['flags'] is None:
            self['flags'] = 0
        else:
            self['flags'] &= ~(self['flags'] & 1)
        return self

    def remove(self):
        '''
        Mark the interface for removal
        '''
        self['ipdb_scope'] = 'remove'
        return self

    def shadow(self):
        '''
        Remove the interface from the OS, but leave it in the
        database. When one will try to re-create interface with
        the same name, all the old saved attributes will apply
        to the new interface, incl. MAC-address and even the
        interface index. Please be aware, that the interface
        index can be reused by OS while the interface is "in the
        shadow state", in this case re-creation will fail.
        '''
        self['ipdb_scope'] = 'shadow'
        return self
