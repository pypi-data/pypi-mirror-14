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

class _PockerFail(Exception):pass

class Volume(object):
    STATES = 'deleted created'.split()

    def __init__(self, docker, vol_opts):
        self.docker = docker
        self.vol_opts = vol_opts
        self.name = vol_opts.get('name')
        self.changed = False

        self._state = None
        volumes = [vol['Name'] for vol in docker.volume_ls().result]
        self.state = 'created' if self.name in volumes else 'deleted'
        self.inspect_data = self.inspect()

    def _create(self):
        self.docker.volume_create(**self.vol_opts)
        self.inspect_data = self.inspect()

    def _delete(self):
        self.docker.volume_rm(self.name)

    def inspect(self):
        if self.state == 'created':
            return self.docker.volume_inspect(self.name).result[0]
        else:
            return None

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


def check_params(p):
    if not p.vol_opts.get('name', None):
        raise _PockerFail(
            "'vol_opts.name' must be specified."
        )


def pocker_vol(params):
    p = params = qdict(params)
    docker = Docker(**p.docker_opts)

    check_params(p)

    states = 'present absent'.split()
    if not (p.state in states):
        raise _PockerFail("Unknown state. State must be one of: {0}".format(states))

    volume = Volume(docker, p.vol_opts)
    getattr(volume, p.state)()

    return qdict({'changed': volume.changed, 'facts': volume.inspect()})


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
                #TODO: need labels support for this?
                    #reloaded
                    #force_reloaded
            vol_opts=dict(type='dict', required=False, default={}),

            docker_opts=dict(type='dict', required=False, default={}),
        ),
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    try:
        result = pocker_vol(module.params)
        module.exit_json(changed=result.changed, ansible_facts={'volumes': result.facts})
    except _PockerFail as e:
        module.fail_json(msg=e.message)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


