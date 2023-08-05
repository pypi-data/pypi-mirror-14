# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import time
import yaml

import netifaces

from libcloud.compute.base import NodeState
from libcloud.compute.deployment import Deployment
from libcloud.compute.deployment import FileDeployment
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment
from libcloud.compute.deployment import SSHKeyDeployment
from libcloud.compute.ssh import SSHClient

from plumbery.exception import PlumberyException
from plumbery.nodes import PlumberyNodes
from plumbery.polisher import PlumberyPolisher
from plumbery.text import PlumberyText
from plumbery.text import PlumberyNodeContext


class FileContentDeployment(Deployment):
    """
    Installs a file on a target node.
    """

    def __init__(self, content, target):
        """
        :type content: ``str``
        :keyword content: Content of the target file to create

        :type target: ``str``
        :keyword target: Path to install file on node
        """
        self.content = content
        self.target = target

    def run(self, node, client):
        """
        Writes the file.

        See also :class:`Deployment.run`
        """
        client.put(path=self.target, contents=self.content)
        return node


class RebootDeployment(Deployment):
    """
    Reboots a node and let cloud-init do the dirty job.
    """

    def __init__(self, container):
        """
        :param container: the container of this node
        :type container: :class:`plumbery.PlumberyInfrastructure`
        """
        self.region = container.region

    def run(self, node, client):
        """
        Reboots the node.

        See also :class:`Deployment.run`
        """
        self.region.reboot_node(node)
        return node


class RubPolisher(PlumberyPolisher):
    """
    Bootstraps nodes via ssh

    This polisher looks at each node in sequence, and contact selected nodes
    via ssh to rub them. The goal here is to accelerate post-creation tasks as
    much as possible.

    Bootstrapping steps can consist of multiple tasks:

    * push a SSH public key to allow for automated secured communications
    * ask for package update
    * install docker
    * install any pythons script
    * install Stackstorm
    * configure a Chef client
    * register a node to a monitoring dashboard
    * ...

    To activate this polisher you have to mention it in the fittings plan,
    like in the following example::

        ---
        safeMode: False
        polishers:
          - rub:
              key: ~/.ssh/id_rsa.pub
        ---
        # Frankfurt in Europe
        locationId: EU6
        regionId: dd-eu
        ...

    Plumbery will only rub nodes that have been configured for it. The example
    below demonstrates how this can be done for multiple docker containers::

        # some docker resources
        - docker:
            domain: *vdc1
            ethernet: *containers
            nodes:
              - docker1:
                  rub: &docker
                    - run rub.update.sh
                    - run rub.docker.sh
              - docker2:
                  rub: *docker
              - docker3:
                  rub: *docker


    In the real life when you have to rub any appliance, you need to be close
    to the stuff and to touch it. This is the same for virtual fittings.
    This polisher has the need to communicate directly with target
    nodes over the network.

    This connectivity can become quite complicated because of the potential mix
    of private and public networks, firewalls, etc. To stay safe plumbery
    enforces a simple beachheading model, where network connectivity with end
    nodes is a no brainer.

    This model is based on predefined network addresses for plumbery itself,
    as in the snippet below::

        ---
        # Frankfurt in Europe
        locationId: EU6
        regionId: dd-eu

        # network subnets are 10.1.x.y
        rub:
          - beachhead: 10.1.3.4

    Here nodes at EU6 will be rubbed only if the machine that is
    executing plumbery has the adress 10.1.3.4. In other cases, plumbery will
    state that the location is out of reach.

    """

    def _apply_rubs(self, node, steps):
        """
        Does the actual job over SSH

        :param node: the node to be polished
        :type node: :class:`libcloud.compute.base.Node`

        :param steps: the various steps of the rubbing
        :type steps: :class:`libcloud.compute.deployment.MultiStepDeployment`

        :return: ``True`` if everything went fine, ``False`` otherwise
        :rtype: ``bool``

        """

        if node is None or node.state != NodeState.RUNNING:
            logging.info("- skipped - node is not running")
            return False

        # select the address to use
        if len(node.public_ips) > 0:
            target_ip = node.public_ips[0]
        elif node.extra['ipv6']:
            target_ip = node.extra['ipv6']
        else:
            target_ip = node.private_ips[0]

        # guess location of user key
        path = os.path.expanduser('~/.ssh/id_rsa')

        # use libcloud to communicate with remote nodes
        session = SSHClient(hostname=target_ip,
                            port=22,
                            username='root',
                            password=self.secret,
                            key_files=path,
                            timeout=9)

        try:
            session.connect()

            if self.engine.safeMode:
                logging.info("- skipped - no ssh interaction in safe mode")

            else:
                node = steps.run(node, session)

        except Exception as feedback:
            logging.info("Error: unable to rub '{}' at '{}'!".format(
                node.name, target_ip))
            logging.error(str(feedback))
            logging.info("- failed")
            result = False

        else:
            result = True

        try:
            session.close()
        except:
            pass

        return result

    def _get_rubs(self, node, settings, container):
        """
        Defines the set of actions to be done on a node

        :param node: the node to be polished
        :type node: :class:`libcloud.compute.base.Node`

        :param settings: the fittings plan for this node
        :type settings: ``dict``

        :param container: the container of this node
        :type container: :class:`plumbery.PlumberyInfrastructure`

        :return: a list of actions to be performed, and related descriptions
        :rtype: a ``list`` of `{ 'description': ..., 'genius': ... }``

        """

        if not isinstance(settings, dict):
            return []

        environment = PlumberyNodeContext(node=node,
                                          container=container,
                                          context=self.facility)

        rubs = []

        if self.key is not None:
            rubs.append({
                'description': 'deploy SSH public key',
                'genius': SSHKeyDeployment(self.key)})

        if ('rub' in settings
                and isinstance(settings['rub'], list)
                and len(settings['rub']) > 0):

            logging.debug('- using rub commands')

            for script in settings['rub']:

                tokens = script.split(' ')
                if len(tokens) == 1:
                    tokens.insert(0, 'run')

                if tokens[0] in ['run', 'run_raw']:  # send and run a script

                    script = tokens[1]
                    if len(tokens) > 2:
                        args = tokens[2:]
                    else:
                        args = []

                    logging.debug("- {} {} {}".format(
                        tokens[0], script, ' '.join(args)))

                    try:
                        path = os.path.dirname(__file__)+'/'+script
                        with open(path) as stream:
                            text = stream.read()

                            if(tokens[0] == 'run'
                                    and PlumberyText.could_expand(text)):

                                logging.debug("- expanding script '{}'"
                                              .format(script))
                                text = PlumberyText.expand_variables(
                                    text, environment)

                            if len(text) > 0:
                                rubs.append({
                                    'description': ' '.join(tokens),
                                    'genius': ScriptDeployment(
                                        script=text,
                                        args=args,
                                        name=script)})

                            else:
                                logging.error("- script '{}' is empty"
                                              .format(script))

                    except IOError:
                        logging.error("- unable to read script '{}'"
                                      .format(script))

                elif tokens[0] in ['put', 'put_raw']:  # send a file

                    file = tokens[1]
                    if len(tokens) > 2:
                        destination = tokens[2]
                    else:
                        destination = './'+file

                    logging.debug("- {} {} {}".format(
                        tokens[0], file, destination))

                    try:
                        source = os.path.dirname(__file__)+'/'+file
                        with open(source) as stream:
                            content = stream.read()

                            if(tokens[0] == 'put'
                                    and PlumberyText.could_expand(content)):

                                logging.debug("- expanding file '{}'"
                                              .format(file))
                                content = PlumberyText.expand_variables(
                                    content, environment)

                            rubs.append({
                                'description': ' '.join(tokens),
                                'genius': FileContentDeployment(
                                    content=content,
                                    target=destination)})

                    except IOError:
                        logging.error("- unable to read file '{}'"
                                      .format(file))

                else:  # echo a sensible message eventually

                    if tokens[0] == 'echo':
                        tokens.pop(0)
                    message = ' '.join(tokens)
                    message = PlumberyText.expand_variables(
                        message, environment)
                    logging.info("- {}".format(message))

        if ('cloud-config' in settings
                and isinstance(settings['cloud-config'], dict)
                and len(settings['cloud-config']) > 0):

            logging.info('- using cloud-config')

            # mandatory, else cloud-init will not consider user-data
            logging.debug('- preparing meta-data')
            meta_data = 'instance_id: dummy\n'

            destination = '/var/lib/cloud/seed/nocloud-net/meta-data'
            rubs.append({
                'description': 'put meta-data',
                'genius': FileContentDeployment(
                    content=meta_data,
                    target=destination)})

            logging.debug('- preparing user-data')

            expanded = PlumberyText.expand_variables(
                settings['cloud-config'], environment)

            user_data = '#cloud-config\n'+expanded
            logging.debug(user_data)

            destination = '/var/lib/cloud/seed/nocloud-net/user-data'
            rubs.append({
                'description': 'put user-data',
                'genius': FileContentDeployment(
                    content=user_data,
                    target=destination)})

            logging.debug('- preparing remote install of cloud-init')

            script = 'rub.cloud-init.sh'
            try:
                path = os.path.dirname(__file__)+'/'+script
                with open(path) as stream:
                    text = stream.read()
                    if text:
                        rubs.append({
                            'description': 'run '+script,
                            'genius': ScriptDeployment(
                                script=text,
                                name=script)})

            except IOError:
                raise PlumberyException("Error: cannot read '{}'"
                                        .format(script))

            logging.debug('- preparing reboot to trigger cloud-init')

            rubs.append({
                'description': 'reboot node',
                'genius': RebootDeployment(
                    container=container)})

        return rubs

    def go(self, engine):
        """
        Starts the rubbing process

        :param engine: access to global parameters and functions
        :type engine: :class:`plumbery.PlumberyEngine`

        """

        super(RubPolisher, self).go(engine)

        self.report = []

        self.secret = engine.get_shared_secret()

        self.key = None
        if 'key' in self.settings:
            try:
                path = os.path.expanduser(self.settings['key'])

                with open(path) as stream:
                    self.key = stream.read()
                    stream.close()

            except IOError:
                pass

    def move_to(self, facility):
        """
        Checks if we can beachhead at this facility

        :param facility: access to local parameters and functions
        :type facility: :class:`plumbery.PlumberyFacility`

        This function lists all addresses of the computer that is running
        plumbery. If there is at least one routable IPv6 address, then
        it assumes that communication with nodes is possible. If no suitable
        IPv6 address can be found, then plumbery falls back to IPv4.
        Beachheading is granted only if the address of the computer running
        plumbery matches the fitting parameter ``beachhead``.
        """

        self.facility = facility
        self.region = facility.region
        self.nodes = PlumberyNodes(facility)

        self.beachheading = False

        try:

            self.addresses = []

            for interface in netifaces.interfaces():
                addresses = netifaces.ifaddresses(interface)

                if netifaces.AF_INET in addresses.keys():
                    for address in addresses[netifaces.AF_INET]:

                        # strip local loop
                        if address['addr'].startswith('127.0.0.1'):
                            continue

                        self.addresses.append(address['addr'])

                if netifaces.AF_INET6 in addresses.keys():
                    for address in addresses[netifaces.AF_INET6]:

                        # strip local loop
                        if address['addr'].startswith('::1'):
                            continue

                        # strip local link addresses
                        if address['addr'].startswith('fe80::'):
                            continue

                        # we have a routable ipv6, so let's go
                        self.beachheading = True

        except Exception as feedback:
            logging.error(str(feedback))

        for item in self.facility.get_parameter('rub', []):
            if not isinstance(item, dict):
                continue
            if 'beachhead' not in item.keys():
                continue
            if item['beachhead'] in self.addresses:
                self.beachheading = True
                break

        if self.beachheading:
            logging.info("- beachheading at '{}'".format(
                self.facility.get_parameter('locationId')))
        else:
            logging.debug("- '{}' is unreachable".format(
                self.facility.get_parameter('locationId')))

    def shine_node(self, node, settings, container):
        """
        Rubs a node

        :param node: the node to be polished
        :type node: :class:`libcloud.compute.base.Node`

        :param settings: the fittings plan for this node
        :type settings: ``dict``

        :param container: the container of this node
        :type container: :class:`plumbery.PlumberyInfrastructure`

        """

        logging.info("Rubbing node '{}'".format(settings['name']))
        if node is None:
            logging.info("- not found")
            return

        timeout = 300
        tick = 6
        while node.extra['status'].action == 'START_SERVER':
            time.sleep(tick)
            node = self.nodes.get_node(node.name)
            timeout -= tick
            if timeout < 0:
                break

        if node.state != NodeState.RUNNING:
            logging.info("- skipped - node is not running")
            return

        rubs = self._get_rubs(node, settings, container)
        if len(rubs) < 1:
            logging.info('- nothing to do')
            self.report.append({node.name: {
                'status': 'skipped - nothing to do'
                }})
            return

        if len(node.public_ips) > 0:
            logging.info("- node is reachable at '{}'".format(
                node.public_ips[0]))

        elif not self.beachheading:
            logging.info('- node is unreachable')
            self.report.append({node.name: {
                'status': 'unreachable'
                }})
            return

        descriptions = []
        steps = []
        for item in rubs:
            descriptions.append(item['description'])
            steps.append(item['genius'])

        if self._apply_rubs(node, MultiStepDeployment(steps)):
            logging.info('- done')
            self.report.append({node.name: {
                'status': 'completed',
                'rubs': descriptions
                }})

        else:
            self.report.append({node.name: {
                'status': 'failed',
                'rubs': descriptions
                }})

    def reap(self):
        """
        Reports on rubbing

        """

        if 'reap' not in self.settings:
            return

        fileName = self.settings['reap']
        logging.info("Reporting on rubs in '{}'".format(fileName))
        with open(fileName, 'w') as stream:
            stream.write(yaml.dump(self.report, default_flow_style=False))
            stream.close()
