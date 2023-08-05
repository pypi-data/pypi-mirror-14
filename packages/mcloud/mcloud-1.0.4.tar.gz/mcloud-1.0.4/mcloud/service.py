import logging
import traceback
from mcloud.plugin import enumerate_plugins
from pprintpp import pprint
import re
import inject
from mcloud.remote import ApiRpcServer
from mcloud.txdocker import IDockerClient, DockerConnectionFailed, DockerTwistedClient
from twisted.internet import defer
from twisted.internet.defer import inlineCallbacks, returnValue
import txredisapi
import os
from zope.interface import Interface
from zope.interface.verify import verifyObject

logger = logging.getLogger('mcloud.application')


class NotInspectedYet(Exception):
    pass


class IServiceBuilder(Interface):
    """
    Allow plugins to participate in container build process.
    """

    def configure_container_on_start(service, config):
        """
        introspect service state and make changes on config dictionary that is passed to Docker
        """

    def configure_container_on_create(service, config):
        """
        introspect service state and make changes on config dictionary that is passed to Docker
        """


class IServiceLifecycleListener(Interface):

    def on_service_start(service, ticket_id=None):
        """
        Called when service is started
        """


class Service(object):

    NotInspectedYet = NotInspectedYet

    settings = inject.attr('settings')
    dns_search_suffix = inject.attr('dns-search-suffix')
    redis = inject.attr(txredisapi.Connection)

    rpc_server = inject.attr(ApiRpcServer)

    plugins = inject.attr('plugins')

    error = False

    def __init__(self, client=None, **kwargs):

        self.api_file = None

        self.client = client
        """
        @type client: DockerTwistedClient
        """

        self.image_builder = None
        self.name = None
        self.app_name = None
        self.entrypoint = None
        self.workdir = None
        self.volumes = []
        self.volumes_from = None
        self.ports = None
        self.web_port = None
        self.ssl_port = None
        self.command = None
        self.env = None
        self.config = None
        self.status_message = ''
        self._inspect_data = None
        self._inspected = False
        self.wait = False

        self._stats = None

        self.__dict__.update(kwargs)
        super(Service, self).__init__()



    def task_log(self, ticket_id, message):
        if not ticket_id:
            print(message)
        else:
            self.rpc_server.task_progress(message + '\n', ticket_id)

    def build_docker_config(self):
        pass


    @inlineCallbacks
    def inspect(self):
        self._inspected = True

        try:
            data = yield self.client.inspect(self.name)
            self._inspect_data = data

            if self.is_running():
                data = yield self.client.stats(self.id)
                self._stats = data

        except DockerConnectionFailed as e:
            self.error = 'Can not connect to docker: %s. %s' % (self.client.url, e)
            self._inspect_data = None

        defer.returnValue(self._inspect_data)

    @property
    def stats(self):
        if not self.is_inspected():
            raise self.NotInspectedYet()

        data = self._stats

        if not data:
            return None

        return {
            'cpu_usage': 100.0 * float(data['cpu_stats']['cpu_usage']['total_usage']) / (data['cpu_stats']['system_cpu_usage']),
            'memory_usage': data['memory_stats']['usage'],
            'memory_limit': data['memory_stats']['limit'],
            'net_rx': data['network']['rx_bytes'],
            'net_tx': data['network']['tx_bytes'],
        }

    @property
    def id(self):
        if not self.is_created():
            return None

        return self._inspect_data['Id']

    def is_running(self):
        if not self.is_inspected():
            raise self.NotInspectedYet()
        try:
            return self.is_created() and self._inspect_data['State']['Running']
        except KeyError:
            return False

    @property
    def id(self):
        if not self.is_created():
            return None

        return self._inspect_data['Id']

    @property
    def shortname(self):
        name_ = self.name
        if self.app_name and name_.endswith(self.app_name):
            name_ = name_[0:-len(self.app_name) - 1]
        return name_

    def ip(self):
        if not self.is_running():
            return None

        return self._inspect_data['NetworkSettings']['IPAddress']

    def image(self):
        if not self.is_created():
            return None

        return self._inspect_data['Image']

    def hosts_path(self):
        if not self.is_created():
            return None

        return self._inspect_data['HostsPath']

    def list_volumes(self):
        if not self.is_created():
            return None

        volumes_ = self._inspect_data['Volumes']

        internal_volumes = (
            # '/var/run/mcloud',
            '/usr/bin/@me'
        )
        for iv in internal_volumes:
            if iv in volumes_:
                del volumes_[iv]

        return volumes_

    def public_ports(self):
        if not self.is_running():
            return None

        return self._inspect_data['NetworkSettings']['Ports']

    def attached_volumes(self):
        if not self.is_running():
            return None

        return self.list_volumes().keys()

    def started_at(self):
        if not self.is_running():
            return None

        return self._inspect_data['State']['StartedAt']

    def is_web(self):
        return not self.web_port is None

    def get_web_port(self):
        return self.web_port

    def is_ssl(self):
        return not self.ssl_port is None

    def error_msg(self):
        return self.error

    def get_ssl_port(self):
        return self.ssl_port

    def is_created(self):
        if not self.is_inspected():
            raise self.NotInspectedYet()

        return not self._inspect_data is None

    def is_internal_volume(self, x):
        return x == '/usr/bin/@me'

    def is_read_only(self, x):
        return self.is_internal_volume(x)

    @inlineCallbacks
    def run(self, ticket_id, command, size=None):

        image_name = yield self.image_builder.build_image(ticket_id=ticket_id, service=self)

        config = yield self._generate_config(image_name, for_run=True)

        config['Cmd'] = command
        config['Tty'] = True
        config['AttachStdin'] = True
        config['AttachStdout'] = True
        config['AttachStderr'] = True
        config['OpenStdin'] = True

        name = '%s_pty_%s' % (self.name, ticket_id)

        yield self.client.create_container(config, name, ticket_id=ticket_id)

        if self.ports:
            config['PortBindings'] = self.prepare_ports()



        if self.volumes and len(self.volumes):
            config['Binds'] = ['%s:%s' % (x['local'], x['remote'] + (':ro' if self.is_read_only(x['remote']) else '')) for x in self.volumes]

        for plugin in enumerate_plugins(IServiceBuilder):
            yield plugin.configure_container_on_start(self, config)

        yield self.client.start_container(name, ticket_id=ticket_id, config=config)

        if size:
            yield self.client.resize(name, width=size[1], height=size[0])
            yield self.client.attach(name, ticket_id)
        else:
            yield self.client.attach(name, ticket_id, skip_terminal=True)

    def prepare_ports(self):
        all_ports = {}
        for port in self.ports:
            if isinstance(port, basestring) and ':' in port:
                local, host = port.split(':')
                if '_' in host:
                    ip, rport = host.split('_')
                else:
                    rport = host
                    ip = None

                all_ports[local] = [{"HostPort": rport, "HostIp": ip}]
            else:
                all_ports[port] = [{}]

        return all_ports

    @inlineCallbacks
    def start(self, ticket_id=None):

        id_ = yield self.client.find_container_by_name(self.name)

        self.task_log(ticket_id, '[%s][%s] Starting service' % (ticket_id, self.name))
        self.task_log(ticket_id, '[%s][%s] Service resolve by name result: %s' % (ticket_id, self.name, id_))

        # container is not created yet
        if not id_:
            self.task_log(ticket_id, '[%s][%s] Service not created. Creating ...' % (ticket_id, self.name))
            yield self.create(ticket_id)
            id_ = yield self.client.find_container_by_name(self.name)

        current_config = yield self.inspect()
        image_id = current_config['Image']
        image_info = yield self.client.inspect_image(image_id)

        self.task_log(ticket_id, '[%s][%s] Starting service...' % (ticket_id, self.name))

        config = {
            # "Dns": [self.dns_server],
            # "DnsSearch": '%s.%s' % (self.app_name, self.dns_search_suffix)
        }

        for plugin in enumerate_plugins(IServiceBuilder):
            yield plugin.configure_container_on_start(self, config)


        if self.volumes_from:
            config['VolumesFrom'] = self.volumes_from

        if self.ports:
            config['PortBindings'] = self.prepare_ports()

        mounted_volumes = []
        config['Binds'] = []
        if self.volumes and len(self.volumes):
            for x in self.volumes:
                mounted_volumes.append(x['remote'])
                config['Binds'].append('%s:%s' % (x['local'], x['remote'] + (':ro' if self.is_read_only(x['remote']) else '')))


        if image_info['ContainerConfig']['Volumes']:
            for vpath, vinfo in image_info['ContainerConfig']['Volumes'].items():

                if not vpath in mounted_volumes:
                    dir_ = os.path.expanduser('%s/volumes/%s/%s' % (self.settings.home_dir, self.name, re.sub('[^a-z0-9]+', '_', vpath)))

                    if self.settings.btrfs:
                        dir_ += '_btrfs'

                    if not os.path.exists(dir_):
                        if self.settings.btrfs:
                            os.system('btrfs subvolume create %s' % dir_)
                        else:
                            os.makedirs(dir_)

                    mounted_volumes.append(vpath)
                    config['Binds'].append('%s:%s' % (dir_, vpath))

        #config['Binds'] = ["/home/alex/dev/mcloud/examples/static_site1/public:/var/www"]

        self.task_log(ticket_id, 'Startng container. config: %s' % config)

        yield self.client.start_container(id_, ticket_id=ticket_id, config=config)

        yield self.inspect()

        if self.is_running():
            content = """
#!/bin/sh

echo -e "\n@mcloud $@\n"
"""

            print 'Load file into container: ' + '/usr/bin/@me'
            yield self.client.put_file(id_, '/usr/bin/@me', content,  ticket_id=ticket_id)

        # lifecycle events

        self.task_log(ticket_id, 'Emit startup event')
        for plugin in enumerate_plugins(IServiceLifecycleListener):
            self.task_log(ticket_id, 'Call start listener %s' % plugin)
            yield plugin.on_service_start(self, ticket_id=ticket_id)

        # inspect and return result
        ret = yield self.inspect()

        defer.returnValue(ret)


    @inlineCallbacks
    def restart(self, ticket_id=None):
        yield self.stop(ticket_id)
        yield self.start(ticket_id)


    @inlineCallbacks
    def rebuild(self, ticket_id=None):
        yield self.stop(ticket_id)
        yield self.destroy(ticket_id)
        yield self.start(ticket_id)


    @inlineCallbacks
    def stop(self, ticket_id=None):

        id = yield self.client.find_container_by_name(self.name)

        yield self.client.stop_container(id, ticket_id=ticket_id)

        ret = yield self.inspect()
        defer.returnValue(ret)


    @inlineCallbacks
    def pause(self, ticket_id=None):

        id = yield self.client.find_container_by_name(self.name)

        yield self.client.pause_container(id, ticket_id=ticket_id)

        ret = yield self.inspect()
        defer.returnValue(ret)


    @inlineCallbacks
    def unpause(self, ticket_id=None):

        id = yield self.client.find_container_by_name(self.name)

        yield self.client.unpause_container(id, ticket_id=ticket_id)

        ret = yield self.inspect()
        defer.returnValue(ret)


    @inlineCallbacks
    def last_logs(self, on_log):
        id = yield self.client.find_container_by_name(self.name)

        yield self.client.logs(self, id, on_log, tail=100, follow=False)

    @inlineCallbacks
    def _generate_config(self, image_name, for_run=False):
        config = {
            "Image": image_name
        }

        image_info = None
        # TODO: improve tests
        if hasattr(self.client, 'inspect_image'):
            image_info = yield self.client.inspect_image(image_name)

        vlist = yield self.redis.hgetall('vars')

        if self.env:
            vlist.update(self.env)

        if len(vlist) > 0:
            config['Env'] = ['%s=%s' % x for x in vlist.items()]


        if self.ports:
            all_ports = {}
            for port in self.ports:
                if isinstance(port, basestring) and ':' in port:
                    all_ports[port.split(':')[0]] = {}
                else:
                    all_ports[port] = {}

            config['ExposedPorts'] = all_ports


        if self.entrypoint:
            config['Entrypoint'] = self.entrypoint

        if self.workdir:
            config['WorkingDir'] = self.workdir

        if not for_run:
            config['Hostname'] = self.name

            if self.command:
                config['Cmd'] = self.command.split(' ')

        for plugin in enumerate_plugins(IServiceBuilder):
            yield plugin.configure_container_on_create(self, config)

        defer.returnValue(config)


    @inlineCallbacks
    def create(self, ticket_id=None):
        image_name = yield self.image_builder.build_image(ticket_id=ticket_id, service=self)

        config = yield self._generate_config(image_name)
        yield self.client.create_container(config, self.name, ticket_id=ticket_id)

        ret = yield self.inspect()
        defer.returnValue(ret)

    @inlineCallbacks
    def destroy(self, ticket_id=None):
        id_ = yield self.client.find_container_by_name(self.name)

        yield self.client.remove_container(id_, ticket_id=ticket_id)

        ret = yield self.inspect()
        defer.returnValue(ret)

    def is_inspected(self):
        return self._inspected




