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


def pocker_cmd(params):
    p = params = qdict(params)
    docker = Docker(**p.docker_opts)

    #TODO: filter containers to apply command
    args = p.cmd_args if p.cmd_args is not None else ''
    resp = getattr(docker, p.cmd)(*shlex.split(args), **p.cmd_opts)
    return resp


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(type='str', required=True),
            cmd_args=dict(type='str', required=False, default=None),
            cmd_opts=dict(type='dict', required=False, default={}),

            docker_opts=dict(type='dict', required=False, default={}),
        ),
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    try:
        resp = pocker_cmd(module.params)
        module.exit_json(changed=True, ansible_facts={"pocker_cmd_result": resp.result}, **resp)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


