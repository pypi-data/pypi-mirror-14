#!/usr/bin/python
# encoding: utf-8

try:
    import pocker
except ImportError:
    HAS_POCKER = False
else:
    HAS_POCKER = True

if HAS_POCKER:
    from pocker import Docker
    from pocker.utils import qdict
    from pocker.exceptions import PExitNonZero

class Network(object):
    STATES = 'deleted created'.split()

    def __init__(self, docker, name, net_opts):
        self.docker = docker
        self.name = name
        self.net_opts = net_opts
        self.changed = False

        self._state = None
        networks = [net['Name'] for net in docker.network_ls().result]
        self.state = 'created' if name in networks else 'deleted'
        self.inspect_data = self.inspect()

    def _create(self):
        self.docker.network_create(self.name, **self.net_opts)
        self.inspect_data = self.inspect()

    def _delete(self):
        for cont in self.containers():
            self.docker.network_disconnect(self.name, cont)
        self.docker.network_rm(self.name)

    def inspect(self):
        if self.state == 'created':
            return self.docker.network_inspect(self.name).result[0]
        else:
            return None

    def containers(self):
        if self.inspect_data:
            return self.inspect_data['Containers'].keys()
        else:
            return []

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if not (state in self.STATES):
            raise Exception('Wrong state: {0} not in {1}'.format(state, self.STATES))

        if self._state != state:
            if self._state is not None:
                self.changed = True
            self._state = state

    def present(self):
        if self.state == 'created':
            return
        if self.state == 'deleted':
            self._create()
        self.state = 'created'

    def absent(self):
        if self.state == 'deleted':
            return
        if self.state == 'created':
            self._delete()
        self.state = 'deleted'

    def set_connections(self, connected, disconnected=[], disconnect_others=False):
        #TODO: connect containers by beacon
        containers = self.containers()
        connected = [cnt['Id'] for cnt in self.docker.inspect(*connected).result] if connected else []
        disconnected = [cnt['Id'] for cnt in self.docker.inspect(*disconnected).result] if disconnected else []

        to_connect = set(connected) - set(containers)
        to_disconnect = set(disconnected) & set(containers)
        others = set(containers) - set(connected) - set(disconnected)

        for cnt in to_connect:
            self.docker.network_connect(self.name, cnt)
            self.changed = True
        for cnt in to_disconnect:
            self.docker.network_disconnect(self.name, cnt)
            self.changed = True

        if disconnect_others:
            for cnt in others:
                self.docker.network_disconnect(self.name, cnt)
                self.changed = True


def pocker_net(params):
    p = params = qdict(params)
    docker = Docker(**p.docker_opts)

    network = Network(docker, p.name, p.net_opts)
    getattr(network, p.state)()
    if p.state != 'absent':
        network.set_connections(p.connected, p.disconnected, p.disconnect_others)

    return qdict({'changed': network.changed, 'facts': network.inspect()})


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', required=True),
                #TODO: need labels support for this?
                    #reloaded
                    #force_reloaded
            connected=dict(type='list', required=False, default=[]),
            disconnected=dict(type='list', required=False, default=[]),
            disconnect_others=dict(type='bool', required=False, default=False),
            net_opts=dict(type='dict', required=False, default={}),

            docker_opts=dict(type='dict', required=False, default={}),
        ),
        mutually_exclusive=[['disconnected','disconnect_others']]
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    try:
        result = pocker_net(module.params)
        module.exit_json(changed=result.changed, ansible_facts={'networks': result.facts})
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


