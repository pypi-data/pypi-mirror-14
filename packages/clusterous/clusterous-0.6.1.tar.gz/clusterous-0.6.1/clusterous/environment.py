# Copyright 2015 Nicta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os.path
import time
from urlparse import urlparse

import requests
import sshtunnel
import marathon
from marathon.models.container import MarathonContainer
from marathon.models.constraint import MarathonConstraint

import helpers
import environmentfile
import defaults


class Environment(object):
    """
    Main class for orchestrating Docker containers to set up an environment
    """
    class LaunchError(Exception):
        pass

    def __init__(self, cluster):
        if not cluster:
            raise ValueError('Environment must be initialised with a Cluster object')
        self._cluster = cluster
        self._logger = logging.getLogger(__name__)

    def launch_from_spec(self, env_file, mesos_wait_time=0):
        """
        Launches an environment based on environment file
        mesos_wait_time is the number of seconds to wait for Mesos to make cluster data
        available immediately after cluster creation
        """

        # Get cluster info and validate resources
        self._logger.debug('Preparing to launch...')
        mesos_data = self._get_mesos_data(mesos_wait_time)
        cluster_info = self._process_mesos_data(mesos_data)

        component_resources = self._calculate_resources(env_file.spec, cluster_info)

        marathon_tunnel = self._cluster.make_controller_tunnel(defaults.marathon_port)
        marathon_tunnel.connect()

        running_components = self._check_for_running_components(component_resources.keys(), marathon_tunnel)

        # If there are no components currently running, proceed
        if not running_components:
            success = False
            # Build image(s) if necessary
            images = env_file.spec['environment']['image']
            build_list = []
            self._logger.info('Checking for Docker images...')
            for image in images:
                info = self._cluster.docker_image_info(image['image_name'])
                if not info:
                    dockerfile_folder = env_file.get_full_path(image['dockerfile'])
                    if not os.path.isfile(os.path.join(dockerfile_folder, 'Dockerfile')):
                        raise self.LaunchError('Could not find a Dockerfile in {0}'.format(image['dockerfile']))

                    build_list.append((dockerfile_folder, image['image_name']))
                else:
                    self._logger.debug('Image "{0}" already exists, no need to build'.format(image['image_name']))

            for item in build_list:
                success = self._cluster.docker_build_image(item[0], item[1])
                if not success:
                    raise self.LaunchError('Problem building image from {0}'.format(item[0]))

            # Copy files
            self._logger.info('Copying files...')
            for item in env_file.spec['environment']['copy']:
                full_local_path = env_file.get_full_path(item)
                status, message = self._cluster.sync_put(full_local_path, '')
                if not status:
                    raise self.LaunchError(message)

            # Do the final checks and perform actual launch
            success = self._launch_components(env_file.spec, component_resources, marathon_tunnel)
        else:
            self._logger.info('Environment already running, not launching anything')
            success = True

        marathon_tunnel.close()
        # Launch wasn't (completely) succesful
        if not success:
            return False, ''

        message = ''
        # Expose tunnel
        if env_file.spec['environment'].get('expose_tunnel'):
            message = self._expose_tunnel(env_file.spec['environment']['expose_tunnel'], cluster_info, component_resources)

        return True, message

    def destroy(self):
        """
        Destroy any running Marathon applications
        """
        tunnel = self._cluster.make_controller_tunnel(defaults.marathon_port)
        tunnel.connect()
        marathon_url = 'http://localhost:{0}'.format(tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)
        app_list = client.list_apps()

        if not app_list:
            self._logger.info('No application to destroy')
            tunnel.close()
            return True

        component_count = len(app_list)

        for app in app_list:
            client.delete_app(app.id, force=True)

        self._logger.debug('Sent delete requests, will wait until all destroyed')

        start_time = time.time()
        elapsed_time = 0
        all_destroyed = False

        while elapsed_time < defaults.app_destroy_timeout:
            app_list = client.list_apps()
            if not app_list:
                all_destroyed = True
                self._logger.debug('All apps destroyed')
                break
            time.sleep(2)
            elapsed_time = time.time() - start_time

        # If timed out without destroying
        if not all_destroyed:
            self._logger.warn('Could not delete all applications')
            tunnel.close()
            return False

        self._logger.info('{0} running applications successfully destroyed'.format(component_count))
        tunnel.close()
        return True

    def scale_app(self, node_name, num_nodes_changed, wait_time=0):
        if num_nodes_changed == 0:
            return True, 'Nothing to change'

        mesos_data = self._get_mesos_data(wait_time)
        cluster_info = self._process_mesos_data(mesos_data)
        if node_name not in cluster_info or 'num_nodes' not in cluster_info[node_name]:
            return True ,'No nodes running, apps removed'

        total_nodes_count = cluster_info[node_name]['num_nodes']
        self._logger.debug('Number of nodes according to Mesos: {0}'.format(total_nodes_count))
        original_nodes_count = total_nodes_count - num_nodes_changed

        # Get info about running apps from Marathon
        marathon_tunnel = self._cluster.make_controller_tunnel(defaults.marathon_port)
        marathon_tunnel.connect()

        node_info = self.get_running_components_by_node(marathon_tunnel=marathon_tunnel)

        if not node_name in node_info:
            return False, 'No app running on ' + node_name
        if len(node_info[node_name]) > 1:
            # Currently this should never happen, as scalable nodes can only
            # have one component
            marathon_tunnel.close()
            return False, 'Scaling not possible because multiple components are running'

        running_instances = node_info[node_name][0]['instance_count']

        instances_per_node = int(float(running_instances) / original_nodes_count)

        # Actual number of instances to scale
        num_instances_changed = instances_per_node * num_nodes_changed
        self._logger.debug('Instances per node: {0}'.format(instances_per_node))

        # Connect to Marathon to make change
        marathon_url = 'http://localhost:{0}'.format(marathon_tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)

        # Tell Marathon to scale app
        client.scale_app(node_info[node_name][0]['app_id'], delta=num_instances_changed, force=True)

        # Log info
        info_format = '{0} {1} running instances of component "{2}"'
        app_name = node_info[node_name][0]['app_id'].strip('/')
        if num_nodes_changed < 0:
            action_str = 'Removed'
        else:
            action_str = 'Added'
        self._logger.info(info_format.format(action_str, abs(num_instances_changed), app_name))

        marathon_tunnel.close()
        return True, 'Success'


    def _get_component_hostname(self, component_name, cluster_info, component_resources):
        """
        Given a component name (corresponding to a Marathon "app" name), and cluster and
        component data, returns a hostname that will be resolved by mesos-dns
        """
        name = component_name.strip('/')
        hostname = None
        # Note that the other option would be to use mesos-dns, but that apparently doesn't
        # work properly until several seconds after the Marathon application starts
        if name in component_resources:
            machine = component_resources[name]['machine']
            hostname = cluster_info[machine]['hostname']
        else:
            raise self.LaunchError('No hostname for component "{0}" could be found'.format(name))

        return hostname

    def _get_mesos_data(self, mesos_wait_time):
        """
        Queries Mesos API and obtains information about cluster. Returns raw Mesos data
        """
        time.sleep(mesos_wait_time)
        mesos_data = None
        with self._cluster.make_controller_tunnel(defaults.mesos_port) as tunnel:
            r = requests.get('http://localhost:{0}/master/state.json'.format(tunnel.local_port))
            mesos_data = r.json()

        return mesos_data

    def _process_mesos_data(self, mesos_data):
        """
        Takes raw Mesos data and transforms into usable data structure containing
        information about all slaves and their exact resources
        """
        # Transform cluster info
        if not 'slaves' in mesos_data:
            raise self.LaunchError('Could not obtain cluster information from Mesos')

        cluster_info = {}

        for host in mesos_data['slaves']:
            if not 'name' in host['attributes']:
                self._logger.warning('No "name" attribute present for mesos slave: {0}'.format(host))
            if not host['attributes']['name'] in cluster_info:
                cluster_info[host['attributes']['name']] = { 'num_nodes': 1,
                                                            'cpus_per_node': host['resources']['cpus'],
                                                            'mem_per_node': host['resources']['mem'],
                                                            'hostname': host['hostname']
                                                            }
            else:
                # Increment node count
                cluster_info[host['attributes']['name']]['num_nodes'] += 1

        return cluster_info


    def _calculate_resources(self, spec, cluster_info):
        """
        Given information about the cluster, processes environment file spec and
        calculates exact resources. I.e. where the user has specified an "auto"
        value, it calculates the exact cpu, memory and instance count of each
        application component

        The high level algorithm:

        For each component
            validate machine type
            Register machine type, cpu, mem

        For each machine type
            for each component, look at cpu and mem requirements
            determine exact cpu and mem for each component

        """

        machines = {}
        component_resources = {}

        # Get requested resources for each machine
        for component_name, vals in spec['environment']['components'].iteritems():
            # Ensure that machine name user has given is valid in this cluster
            if not vals['machine'] in cluster_info:
                raise self.LaunchError('In component "{0}", machine "{1}" '
                                        'does not match any in cluster'.format(
                                        component_name, vals['machine']))

            # Determine auto type
            auto_type = None
            if vals['cpu'] == 'auto':
                auto_type = 'cpu'
            elif vals['count'] == 'auto':
                auto_type = 'count'
            elif vals['cpu'] == 'auto' and vals['count'] == 'auto':
                # Invalid, cannot have auto cpu and auto count
                raise self.LaunchError('For component "{0}", both cpu and count '
                                        'are "auto", which is an invalid '
                                        'combination'.format(component_name))
            else:
                raise self.LaunchError('For component "{0}", cpu is explicitly set to {1} '
                                        'and count to {2}, which is an invalid combination'.format(
                                        component_name, vals['cpu'], vals['count']))
            # Register requested resources for each machine group
            if vals['machine'] not in machines:
                machines[vals['machine']] = {'auto_type': auto_type, 'components': []}

            # The auto type for all components of a machine must be the same
            # If they are mixed, throw an error
            if auto_type != machines[vals['machine']]['auto_type']:
                raise self.LaunchError('Cannot mix components with automatic '
                                        'CPU and automatic Count running on the '
                                        'same machine: {0}'.format(vals['machine']))


            machines[vals['machine']]['components'].append(  {'name':component_name,
                                                'cpu':vals['cpu'], 'count':vals['count']})
        # Determine exact cpu, memory and instance count for each component
        for machine_name, machine_components in machines.iteritems():
            if machine_components['auto_type'] == 'cpu':
                num_components = float(len(machine_components['components']))
                for c in machine_components['components']:
                    resources = {'cpu': cluster_info[machine_name]['cpus_per_node'] / num_components,
                                 'mem': cluster_info[machine_name]['mem_per_node'] / num_components,
                                 'instances': c['count'],
                                 'machine': machine_name
                                 }
                    component_resources[c['name']] = resources
            elif machine_components['auto_type'] == 'count':
                for c in machine_components['components']:
                    cpus_per_node = cluster_info[machine_name]['cpus_per_node']
                    mem_per_cpu = cluster_info[machine_name]['mem_per_node'] / cpus_per_node

                    if c['cpu'] > cpus_per_node:
                        raise self.LaunchError('Component "{0}" is requesting cpu of {1}, but machine '
                                                'type "{2}" only has cpu of {3}'.format(
                                                c['name'], c['cpu'], machine_name, cpus_per_node))

                    # If say there are 2 nodes of 1 cpu each, and each instance requests
                    # 0.4 cpu, there can only be 4 instances running, because cpu
                    # cannot be split across nodes. This handles such situations:

                    # Given requested cpu, the actual number of instances that will run on each node
                    possible_instances_per_node = int(float(cpus_per_node) / c['cpu'])
                    # Amount of cpu that will actually get used in each node (float)
                    possible_cpu_per_node = float(possible_instances_per_node) * c['cpu']

                    # If there is a major difference between what is available and what
                    # will get used, tell the user
                    if (float(cpus_per_node) - possible_cpu_per_node) > 0.05:
                        self._logger.info('Component "{0}" is requesting cpu of {1}, resulting '
                                          'in resources being underused'.format(
                                          c['name'], c['cpu']))

                    resources = {'cpu': c['cpu'],
                                 'mem': mem_per_cpu * float(c['cpu']),
                                 'instances': int(cluster_info[machine_name]['num_nodes'] * possible_instances_per_node),
                                 'machine': machine_name
                                 }
                    component_resources[c['name']] = resources


        return component_resources

    def _check_for_running_components(self, component_names, marathon_tunnel):
        """
        Given a list of component names and a SSHTunnel to Marathon, checks if
        any of the components are running.
        Returns list of those components found to be already running
        """
        marathon_url = 'http://localhost:{0}'.format(marathon_tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)
        app_list = client.list_apps()
        running_components = []
        for app_name in [ a.id.strip('/') for a in app_list ]:
            if app_name in component_names:
                running_components.append(app_name)

        return running_components

    def get_running_components_by_node(self, marathon_tunnel=None):
        """
        Queries Marathon and gets names of each running component by worker, and number
        of instances of each
        """
        tunnel_created = False
        if not marathon_tunnel:
            tunnel = self._cluster.make_controller_tunnel(defaults.marathon_port)
            tunnel.connect()
            tunnel_created = True
        else:
            tunnel = marathon_tunnel

        marathon_url = 'http://localhost:{0}'.format(tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)

        app_list = client.list_apps()
        node_info = {}
        for app in app_list:
            if not app.constraints:
                continue
            con = app.constraints[0]
            if con.field == 'name' and con.operator == 'CLUSTER':
                if con.value not in node_info:
                    node_info[con.value] = [{'app_id': app.id,
                                            'instance_count': app.instances
                                            }]
                else:
                    node_info[con.value].append({'app_id': app.id,
                                                'instance_count': app.instances
                                                })
        if tunnel_created:
            # If a tunnel was created here, close it before returning
            tunnel.close()

        return node_info


    def get_running_component_info(self, marathon_tunnel=None):
        """
        Queries Marathon and gets names of each running component and number of instances
        of each
        """
        tunnel_created = False
        if not marathon_tunnel:
            tunnel = self._cluster.make_controller_tunnel(defaults.marathon_port)
            tunnel.connect()
            tunnel_created = True
        else:
            tunnel = marathon_tunnel

        marathon_url = 'http://localhost:{0}'.format(tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)
        app_list = client.list_apps()
        app_counts = {}
        for app_name in [ a.id.strip('/') for a in app_list ]:
            if app_name not in app_counts:
                app_counts[app_name] = 0
            app_counts[app_name] += client.get_app(app_name).instances

        if tunnel_created:
            # If a tunnel was created here, close it before returning
            tunnel.close()
        return app_counts

    def _launch_components(self, spec, component_resources, tunnel):
        """
        Takes processed component resources dictionary and performs final steps,
        prepares Marathon data structures and launches components.
        Returns when all components are in started state

        High level algorithm:

        For each component
            normalise cmd path
            generate ports list
            validate dependency text
            prepare shared volume
            create port mapping object
            prepare constraint

        For each prepared component
            submit to Marathon API

        Wait until all components are in started state
        """
        volume_mapping = [{ 'mode': 'RW',
                            'containerPath': defaults.shared_volume_path,
                            'hostPath': defaults.shared_volume_path}]
        app_containers = []
        for name, c in spec['environment']['components'].iteritems():
            # Create ports mappings
            port_mappings = []

            if c['ports']:
                # TODO: this validation should happen befor this point
                if not isinstance(c['ports'], basestring):
                    raise self.LaunchError('In component "{0}", "ports" must be a '
                                            'string value'.format(name))
                for p in c['ports'].split(','):
                    port = p.strip()
                    pair = port.split(':')
                    container_port = host_port = 0
                    if len(pair) == 2:
                        host_port = int(pair[0])
                        container_port = int(pair[1])
                    elif len(pair) == 1:
                        container_port = host_port = int(pair[0])
                    else:
                        raise self.LaunchError('In "{0}", malformed port '
                                                'value: {1}'.format(name, pair))
                    port_mappings.append({  'containerPort': container_port,
                                            'hostPort': host_port,
                                            'protocol': 'tcp'})


            # Validate and generate dependencies
            dependencies = []
            constraints = []
            if c['depends']:
                for d in c['depends'].split(','):
                    depend_str = d.strip()
                    if not depend_str in spec['environment']['components']:
                        raise self.LaunchError('Could not find dependency "{0}" as '
                                                'specified in component "{1}"'.format(depend_str, name))
                    dependencies.append('/{0}'.format(depend_str))

            parameters = []
            central_logging_ip = self._cluster.get_central_logging_ip()
            if central_logging_ip:
                parameters.append({ "key": "add-host", "value": 'central-logging:{0}'.format(central_logging_ip) })

            docker = {  'image': c['image'], 'port_mappings': port_mappings,
                        'force_pull_image': True, 'network': c['docker_network'].upper(), 'privileged': True,
                        'parameters': parameters}
            container = MarathonContainer(docker=docker, volumes=volume_mapping)

            if c['machine']:
                constraints = [MarathonConstraint(field='name', operator='CLUSTER', value=c['machine'])]

            app_containers.append({ 'name': name,
                                    'container': container,
                                    'cmd': c['cmd'],
                                    'dependencies': dependencies,
                                    'constraints': constraints})

        # Launch containers

        marathon_url = 'http://localhost:{0}'.format(tunnel.local_port)
        client = marathon.MarathonClient(servers=marathon_url, timeout=600)
        for container in app_containers:
            # Check if app already exists
            app_list = client.list_apps()
            if container['name'] in [ a.id.strip('/') for a in app_list ]:
                raise self.LaunchError('Found a running component named "{0}". '
                                        'Is an environment is already '
                                        'running?'.format(container['name']))
            res = component_resources[container['name']]

            in_str = 'instance' if res['instances'] == 1 else 'instances'
            self._logger.info('Starting {0} {1} of {2}'.format(res['instances'],
                                in_str, container['name']))

            app = client.create_app(container['name'],
                    marathon.models.MarathonApp(cmd=container['cmd'],
                                                dependencies=container['dependencies'],
                                                mem=res['mem'],
                                                cpus=res['cpu'],
                                                instances=res['instances'],
                                                container=container['container'],
                                                constraints=container['constraints']
                                                ))



        # Wait for applications to start running
        self._logger.debug('Waiting for components to start up...')
        expected_containers = len(app_containers)
        running_containers = []
        start_time = time.time()
        elapsed_time = 0
        while (elapsed_time < defaults.app_launch_start_timeout and
               len(running_containers) < expected_containers):
            time.sleep(3)
            for container in app_containers:
                name = container['name']
                if name in running_containers:
                    continue

                app = client.get_app(name)

                # Examine Marathon tasks
                if (app.tasks and
                    len(app.tasks) == component_resources[name]['instances']):
                    all_tasks_running = True
                    # Ensure that all tasks (instances) are running
                    for task in app.tasks:
                        if not task.started_at:
                            # If at least 1 task is not running
                            all_tasks_running = False
                            break
                    if all_tasks_running:
                        running_containers.append(name)

            elapsed_time = time.time() - start_time


        success = True
        launched = ', '.join(running_containers)

        if elapsed_time >= defaults.app_launch_start_timeout:
            self._logger.warning('Timed out waiting for components to launch')
            self._logger.warning('One or more containers are either have problems '
                                 'or are are taking very long to start')
            success = False

        if len(running_containers) < expected_containers:
            self._logger.warning('Could not launch all components')
            success = False

        self._logger.info('Launched {0} components: {1}'.format(len(running_containers), launched))

        return success


    def _expose_tunnel(self, tunnel_info, cluster_info, component_resources):

        tunnel_info_list = []
        message_list = []
        # Determine if it is a dictionary (single tunnel) or a list of dictionaries (1+ tunnels)
        if type(tunnel_info) == dict:
            tunnel_info_list.append(tunnel_info)
        elif type(tunnel_info) == list:
            tunnel_info_list = tunnel_info

        for info in tunnel_info_list:
            parts = info['service'].split(':')

            # Validate port value
            if ( len(parts) != 3 or
                 not parts[0].isdigit() or
                 not parts[2].isdigit()):
                raise self.LaunchError('Invalid syntax: "{0}" Tunnel service must be in '
                                        'the format "localport:component:remoteport"'.format(
                                        info['service']))

            local_port, component_name, remote_port = parts

            hostname = self._get_component_hostname(component_name, cluster_info, component_resources)

            # Make tunnel from controller to node. Note that this uses the same port for both
            # the node and for the controller for simplicity of implementation
            self._cluster.make_tunnel_on_controller(remote_port, hostname, remote_port)

            # Make tunnel from localhost to controller
            success = self._cluster.create_permanent_tunnel_to_controller(remote_port, local_port)

            if not success:
                raise self.LaunchError('Could not create tunnel')

            # Make message
            message = ''
            if info.get('message', ''):
                message = info['message']
                if '{url}' in message:
                    url = 'http://localhost:{0}'.format(local_port)
                    message = message.replace('{url}', url)
                if '{port}' in message:
                    message = message.replace('{port}', local_port)
            else:
                # Default message
                message = 'Tunnel created on port {}'.format(local_port)

            message_list.append(message)

        return '\n'.join(message_list)
