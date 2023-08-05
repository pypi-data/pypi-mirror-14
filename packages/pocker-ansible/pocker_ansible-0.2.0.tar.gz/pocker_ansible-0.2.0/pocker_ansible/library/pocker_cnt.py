#!/usr/bin/python
# encoding: utf-8
import json
import shlex
from copy import deepcopy, copy

try:
    import pocker
except ImportError:
    HAS_POCKER = False
else:
    HAS_POCKER = True

if HAS_POCKER:
    from pocker import Docker
    from pocker.utils import qdict, wait_net_service
    from pocker.exceptions import PExitNonZero

class _PockerFail(Exception):pass

class GroupManager(object):
    def __init__(self, beacon, count, attach, kill_on_stop, docker, opts, img, cmd):
        self.beacon = beacon
        self.count = count
        self.docker = docker
        self.opts = opts
        self.img = img
        self.cmd = cmd
        self.attach = attach

        if img:
            img_inspect = self.docker.inspect(self.img).result
            if not img_inspect: #no image on host
                self.docker.pull(self.img)
                img_inspect = self.docker.inspect(self.img).result
            self.img_info = img_info = img_inspect[0]
        else:
            self.img_info = {'Id': None}

        if count == 1 and opts.get('name', None) and beacon is None:
            beacon = opts.get('name')
            containers_on_host = docker.ps(all=True).result
            for container in containers_on_host:
                if container['Name'] == opts.get('name'):
                    containers_list = [container]
                    break
            else:
                containers_list = []

        else:
            containers_list = docker.ps(all=True, filter="label={0}".format(Container.label('_beacon', beacon))).result

        container_conf = beacon, attach, kill_on_stop, docker, opts, img, cmd, self.img_info['Id']
        if self.count is None:
            self.count = len(containers_list)
        self.containers = self._get_containers(containers_list, container_conf, img)

    def _get_containers(self, containers_list, container_conf, img):
        inspections = []
        if containers_list:
            inspections = self.docker.inspect(*(item['Id'] for item in containers_list)).result
        [inspect.update({'pocker._state': Container.get_state(inspect)}) for inspect in inspections]
        containers = [Container(*container_conf, inspect_data=inspect)
                      for inspect in inspections]
        if len(containers) < self.count:
            inspect_data={'pocker._state': 'deleted'}
            #if img is not specified - use signature from present containers to create new
            if img is None:
                if len(inspections) == 0:
                    raise _PockerFail(
                        "Image for container isn't specified and there is no "
                        "existent container to get 'signature' with 'img' and 'options' from.\n"
                        "\n"
                        "Аre you trying to change state of container that didn't exists?\n"
                        "   To create container provide at least 'cnt_img' or ensure that\n"
                        "   container exists if you want just to change state of container.\n"
                        "Аre you trying to create more containers based on already present "
                        "contianers?\n"
                        "   For that there must be present at least one contianer with\n"
                        "   specified 'beacon'({0})"
                        "".format(self.beacon)
                    )

                inspect_data['Config'] = {'Labels': {}}
                inspect_data['Config']['Labels']['pocker._signature'] = inspections[0]['Config']['Labels']['pocker._signature']

            containers += [Container(*container_conf, inspect_data=deepcopy(inspect_data))
                           for _ in range(0, self.count - len(containers))]
        return containers

    def converge_states(self, states, order=None, filters=None):
        containers = self.get_filtered_containers(self.containers, filters)
        containers = self.get_ordered_containers(containers, order)

        goal = {}
        state_for_leftover = states.pop('leftover', None)
        for state, count in self.get_states_in_order(states):
            goal[state], containers = containers[:count], containers[count:]

        leftover_containers = containers

        for state, containers in goal.items():
            getattr(self, state)(containers)

        if state_for_leftover:
            getattr(self, state_for_leftover)(leftover_containers)

    @staticmethod
    def _filter_by_state(states):
        def filter_func(item):
            return item.state in states
        return filter_func

    def get_filtered_containers(self, containers, filters):
        if filters:
            if filters.get('state', None):
                if not all([state in Container.STATES for state in filters.get('state')]):
                    raise _PockerFail(
                        "In filtering by 'state' kwarg must be "
                        "list of container states. Possible states: {0}"
                        "".format(Container.STATES)
                    )
            #TODO: filter by start time and etc?
            #TODO: filter by multiple parameters
            filter_by, filtering = filters.popitem()
            return filter(getattr(self, '_filter_by_'+filter_by)(filtering), containers)
        else:
            return filter(lambda _: True ,containers)

    @staticmethod
    def _order_by_state(ordering):
        def order_func(item):
            try:
                i = ordering.index(item.state)
            except ValueError:
                i = len(ordering) + 1
            i += 1
            return i
        return order_func

    def get_ordered_containers(self, containers, order):
        if order:
            if order.get('state', None):
                if not all([state in Container.STATES for state in order.get('state')]):
                    raise _PockerFail(
                        "In ordering by 'state' kwarg must be "
                        "list of container states. Possible states: {0}"
                        "".format(Container.STATES)
                    )
            #TODO: order by start time and etc?
            #TODO: order by multiple parameters
            order_by, ordering = order.popitem()
            return sorted(containers, key=getattr(self, '_order_by_'+order_by)(ordering))
        else:
            return sorted(containers, key=lambda _: 0)

    @staticmethod
    def get_states_in_order(states):
        states_order = [
            'present', 'started', 'restarted', 'paused',
            'stopped', 'reloaded', 'force_reloaded',
            'killed', 'absent'
        ]

        for state in states_order:
            count = states.get(state, None)
            if count:
                yield state, count


    def present(self, to_present):
        for container in to_present:
            if container.state == 'deleted':
                container.created()

    def started(self, to_start):
        for container in to_start:
            container.running()

    def restarted(self, to_restart):
        for container in to_restart:
            container.stopped()
            container.running()

    def paused(self, to_pause):
        for container in to_pause:
            container.paused()

    def stopped(self, to_stop):
        for container in to_stop:
            container.stopped()

    def reloaded(self, to_reload, force_reload=False):
        if not force_reload and self.img_info['Id'] is None:
            raise _PockerFail("Container image must be set for state=reloaded")

        for container in to_reload:
            if force_reload or container.need_reload():
                container.deleted()
            container.running(forced_reload=force_reload)

    def force_reloaded(self, to_reload):
        self.reloaded(to_reload, force_reload=True)

    def killed(self, to_kill):
        for container in to_kill:
            container.killed()

    def absent(self, to_delete):
        for container in to_delete:
            container.deleted()


class Container(object):
    def __init__(self, beacon, attach, kill_on_stop, docker, opts, img, cmd, img_id, inspect_data):
        self._state = None
        self.changed = False
        self.beacon, self.docker = beacon, docker
        self.attach = attach
        self.kill_on_stop = kill_on_stop
        self.opts, self.img = deepcopy(opts), img
        self.cmd, self.inspect_data = cmd, inspect_data
        self.img_id = img_id
        self.state = inspect_data.pop('pocker._state')

        #needed for 'force_reloaded'
        self.initial_signature = self._get_signature(inspect_data)

        self.goal_signature = self.make_signature(self.opts, {'img_id': img_id,
                                                              'command': self.cmd})

    def _create(self, reload_was_forced=False):
        if self.img is None:
            signature_copy = deepcopy(self.initial_signature)
            self.cmd = signature_copy.pop('command', '')
            self.img = signature_copy.pop('img_id')
            self.opts = signature_copy
            signature = self.initial_signature
        else:
            signature = self.goal_signature

        self.add_label('_beacon', self.beacon)
        self.add_label('_signature', signature)
        cmd = self.cmd if self.cmd is not None else ''
        cnt_id = self.docker.create(self.img, *shlex.split(cmd), **self.opts).result['Id']

        self.inspect_data = self.docker.inspect(cnt_id).result[0]

    def _start(self):
        self.docker.start(self.id, attach=self.attach)

    STATES = 'deleted created_or_stopped running paused restarting'.split()

    def __str__(self):
        return u"Container state={0}".format(self.state)

    def __repr__(self):
        return str(self)

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


    @property
    def id(self):
        try:
            return self.inspect_data['Id']
        except KeyError:
            return None

    @property
    def present_signature(self):
        return self._get_signature(self.inspect_data)

    def _get_signature(self, inspect_data):
        try:
            return json.loads(inspect_data['Config']['Labels']['pocker._signature'])
        except KeyError:
            return None

    @classmethod
    def make_signature(cls, *args):
        signature = {}
        for d in args:
            signature.update(d)
        return signature

    # след. методы переводят контейнер непосредственно заданное состояние
    # т.е. если вызвать stopped для отсутствующего контейнера, то он создасться,
    # запуститься, а затем остановиться
    def created(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state in ('running', 'restarting'):
            self.stopped()
            self.deleted()
        if self.state == 'deleted':
            self._create()
        self.state = 'created_or_stopped'

    def stopped(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state in ('running', 'restarting'):
            if self.kill_on_stop:
                self.docker.kill(self.id)
            else:
                self.docker.stop(self.id)
        if self.state == 'deleted':
            self._create()
            self._start()
            if self.kill_on_stop:
                self.docker.kill(self.id)
            else:
                self.docker.stop(self.id)
        self.state = 'created_or_stopped'

    def killed(self):
        if self.state == 'created_or_stopped':
            return
        if self.state == 'paused':
            self.running()
        if self.state in ('running', 'restarting'):
            self.docker.kill(self.id)
        if self.state == 'deleted':
            self._create()
            self._start()
            self.docker.kill(self.id)
        self.state = 'created_or_stopped'

    def running(self, forced_reload=False):
        if forced_reload:
            if self.state != 'deleted':
                raise Exception(
                    "'forced_reload' kwarg can be used only if "
                    "container is in deleted state. Use 'container.deleted()' "
                    "before 'container.running(forced_reload=True)'"
                )
        if self.state == 'running':
            return
        if self.state == 'restarting':
            self.stopped()
        if self.state == 'paused':
            self.docker.unpause(self.id)
        if self.state == 'created_or_stopped':
            self.docker.start(self.id)
        if self.state == 'deleted':
            self._create(reload_was_forced=forced_reload)
            self._start()
        self.state = 'running'

    def deleted(self):
        if self.state == 'deleted':
            return
        if self.state == 'paused':
            self.running()
        if self.state in ('running', 'restarting'):
            self.stopped()
        if self.state == 'created_or_stopped':
            self.docker.rm(self.id)
        self.state = 'deleted'
        self.inspect_data = {}

    def paused(self):
        if self.state == 'paused':
            return
        if self.state == 'deleted':
            self.running()
        if self.state == 'created_or_stopped':
            self.running()
        if self.state == 'restarting':
            self.running()
        if self.state == 'running':
            self.docker.pause(self.id)
        self.state = 'paused'

    def need_reload(self):
        #проверяем совпадают ли "подписи" существующего контейнера и "желаемого"
        return not (self.goal_signature == self.present_signature)

    def add_label(self, name, value):
        opts = self.opts
        label = self.label(name, value)
        if not opts.get('label'):
            opts['label'] = label
        else:
            if isinstance(label, list):
                opts['label'].append(label)
            else:
                opts['label'] = [opts['label'], label]

    @classmethod
    def get_state(cls, inspect_data):
        # deleted, created_or_stopped, paused, restarting, running
        if not inspect_data:
            return 'deleted'
        elif inspect_data['State']['Paused']:
            return 'paused'
        elif inspect_data['State']['Restarting']:
            return 'restarting'
        elif inspect_data['State']['Running']:
            return 'running'
        else:
            return 'created_or_stopped'

    @classmethod
    def label(cls, name, value):
        return "pocker.{0}={1}".format(name, json.dumps(value))


def check_params(p):
    if not p.beacon and not p.cnt_opts.get('name'):
        raise _PockerFail(
            "'beacon' or 'cnt_opts.name' must be specified."
        )

    if p.cnt_opts.get('name', None) and (p.count not in (1, None)):
        raise _PockerFail(
            "If 'cnt_opts.name' specified - count must be '1' or None."
        )

    if p.wait_for:
        wait_for_ports = p.wait_for.get('ports', None)
        if not isinstance(wait_for_ports, list) or not wait_for_ports:
            raise _PockerFail(
                "'ports' must be non-empty list. "
                "Instead got: value {0} of type {1}"
                "".format(wait_for_ports, type(wait_for_ports))
            )

    if p.cnt_opts.get('env', None):
        env = p.cnt_opts.get('env', None)
        if not isinstance(env, list) or not env:
            raise _PockerFail(
                "'cnt_opts.env' must be list of strings. "
                "Instead got: value {0} of type {1}. "
                "Use 'pocker_env' filter."
                "".format(env, type(env))
            )
        if not all([isinstance(var, basestring) for var in env]):
            raise _PockerFail(
                "Non string value in 'cnt_opts.env': "
                "value {0} of type {1}. "
                "".format(env, type(env))
            )

def wait_for_services(p, facts):
    if p.wait_for:
        timeout = p.wait_for.get('timeout', 5)
        wait_for_ports = p.wait_for.get('ports')
        for cnt_inspect in facts:
            ip = cnt_inspect['NetworkSettings']['IPAddress']
            #TODO: check version of docker
            if not ip: #for docker 1.9
                for name, network in cnt_inspect['NetworkSettings']['Networks'].items():
                    ip = network['IPAddress']
                    break #use first network to get ipaddres

            exposed_ports = cnt_inspect['NetworkSettings']['Ports']
            exposed_ports = [int(port.split('/')[0]) for port in exposed_ports.keys()]
            for port in wait_for_ports:
                if port not in exposed_ports:
                    raise _PockerFail(
                        "Port stated in 'wait_for.ports'({0}) "
                        "not present in container exposed ports: {1}"
                        "".format(port, exposed_ports)
                    )

                if not wait_net_service(ip, port, timeout):
                    raise _PockerFail(
                        "Exceeded wait_for_timeout(=={2}s) on port '{0}' "
                        "for container '{1}'"
                        "".format(port, cnt_inspect['Id'], timeout)
                    )
        return True
    else:
        return False


def pocker_cnt(params):
    p = params = qdict(params)

    if p.states:
        p.count = sum([val for val in p.states.values() if isinstance(val, int)])
    else:
        if p.count == 'all':
            p.count = None
        if p.count is None:
            p.states = {'leftover': p.state}
        else:
            p.states = {p.state: p.count}

    if p.cnt_opts.get('name', None):
        if p.count is None:
            p.count = 1

    check_params(p)

    docker = Docker(**p.docker_opts)

    manager = GroupManager(p.beacon, p.count, p.attach, p.kill_on_stop,
                           docker, p.cnt_opts, p.cnt_img, p.cnt_cmd)
    if p.state is not None:
        states = 'present started reloaded force_reloaded restarted stopped killed absent paused'.split()
        if not (p.state in states):
            raise _PockerFail("Unknown state. State must be one of: {0}".format(states))

    manager.converge_states(p.states, p.order, p.filters)

    changed = any([cnt.changed for cnt in manager.containers])

    containers = [str(cnt.id) for cnt in manager.containers if cnt.id]

    if containers:
        facts = docker.inspect(*containers).result
    else:
        facts = []

    if wait_for_services(p, facts):
        #update inspection info
        if containers:
            facts = docker.inspect(*containers).result
        else:
            facts = []

    logs = []
    if p.get_logs:
        for cnt in containers:
            logs.append(docker.logs(cnt).stdout_raw)

    #TODO: возвращать что изменилось
    return qdict({'changed': changed, 'facts': facts, 'logs': logs})

def main():
    module = AnsibleModule(
        argument_spec=dict(
            beacon=dict(type='str', required=False, default=None),

            order=dict(type='dict', required=False, default=None),
            filters=dict(type='dict', required=False, default=None),

            states=dict(type='dict', required=False, default={}),

            state=dict(type='str', required=False, default=None),
            count=dict(required=False, default=None),
                # не используем type='int', чтобы можно было передать None или 'all'

            kill_on_stop=dict(type='bool', required=False, default=False),

            cnt_opts=dict(type='dict', required=False, default={}),
            cnt_img=dict(type='str', required=False, default=None),
            cnt_cmd=dict(type='str', required=False, default=None),
            attach=dict(type='bool', required=False, default=False),
            wait_for=dict(type='dict', required=False, default={}),
            get_logs=dict(type='bool', required=False, default=False),

            #common
            docker_opts=dict(type='dict', required=False, default={}),
        ),
        required_one_of=[['states', 'state']],
        mutually_exclusive=[['states','state']]
    )

    if not HAS_POCKER:
        module.fail_json(msg="Can't import 'pocker' lib. Is it installed on this host?")

    try:
        result = pocker_cnt(module.params)
        module.exit_json(changed=result.changed,
                         ansible_facts={'containers': result.facts,
                                        'logs': result.logs})

    except _PockerFail as e:
        module.fail_json(msg=e.message)
    except PExitNonZero as e:
        module.fail_json(msg=e.resp.stderr_raw)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()


