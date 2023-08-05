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

def pocker_img(params):
    p = params = qdict(params)
    docker = Docker(**p.docker_opts)

    image = p.image.strip()
    tag = None
    if ':' in image:
        repo, tag = image.split(':')

    if not tag:
        raise _PockerFail('Tag for image must be specified. Got: {0}'. format(image))

    if p.state == 'absent': #removed from host
        #TODO: это только сделает untag, нужно ли делать доп опцию, чтобы полностью удалить?
        changed = True
        try:
            resp = docker.rmi(image)
        except PExitNonZero as err:
            resp = err.resp
            if 'No such image:' in resp.stderr_lines[0]:
                changed = False
            elif 'could not find image' in resp.stderr_lines[0]:
                changed = False
            else:
                raise err
        #TODO: feedback: was new image deleted, untagged?
        return qdict(changed=changed, **resp)
    elif p.state == 'present': #presented on host, if not - pull image
        images = []
        [images.extend(img['RepoTags'] + img['RepoDigests']) for img in docker.images().result]
        if image in images:
            return qdict(msg="Image already present on host.")
        else:
            resp = docker.pull(image)
            #TODO: feedback: was new image pulled?
            return qdict(**resp)
    elif p.state == 'updated': #images updated from registry
        resp = docker.pull(image)
        #TODO: feedback: was new image pulled?
        return qdict(**resp)
    elif p.state == 'published': #image pushed to registry
        raise _PockerFail('state=published - not implemented yet')
    else:
        raise _PockerFail("Unknown state. Got: {0}. Must be one of: (absent, present, updated, published)".format(p.state))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
            image=dict(type='str', required=True),

            docker_opts=dict(type='dict', required=False, default={}),
        ),
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    try:
        result = pocker_img(module.params)
        module.exit_json(**result)
    except _PockerFail as e:
        module.fail_json(msg=e.message)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


