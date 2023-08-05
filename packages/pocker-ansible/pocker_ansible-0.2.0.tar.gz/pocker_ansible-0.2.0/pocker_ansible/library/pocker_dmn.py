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

def main():
    #WARNING: this module is untested and never used in production!
    #наверное это задача модуля services, но иногда может быть полезно
    #TODO:
    #   - перезапуск, если настройки изменились
    #   - в запущенном состоянии
    #   - в остановленном состоянии
    module = AnsibleModule(
        argument_spec=dict(
            daemon_opts=dict(type='dict', required=False, default={}),
        ),
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    p = params = qdict(module.params)
    docker = Docker(**p.daemon_opts)

    try:
        resp = docker.daemon()
        module.exit_json(**resp)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


