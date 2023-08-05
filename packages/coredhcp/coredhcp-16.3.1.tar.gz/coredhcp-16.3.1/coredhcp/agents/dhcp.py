"""
Copyright (c) 2016 Marta Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from corecluster.agents.base_agent import BaseAgent
from corecluster.utils.logger import *
from corenetwork.utils import system
import os
import subprocess


class AgentThread(BaseAgent):
    task_type = 'dhcp'
    supported_actions = ['start_dhcp', 'stop_dhcp']


    def start_dhcp(self, task):
        network = task.get_obj('Subnet')

        self.stop_dhcp(task)

        gateway = network.get_prop('gateway', None)
        if gateway is None:
            #TODO: Exception?
            return

        system.call(['ip', 'link', 'set', network.isolated_port_name, 'up'], netns=network.netns_name)
        system.call(['ip', 'addr', 'add', 'dev', network.isolated_port_name, '%s/%d' % (gateway, network.mask)], netns=network.netns_name)

        dnsmasq = ['dnsmasq',
                   '-O', '3',
                   '-O', '6',
                   '-i', network.isolated_port_name,
                   '-F', '%s,%s' % (str(network.to_ipnetwork().ip+1), str(network.to_ipnetwork().broadcast-1))]

        for lease in network.lease_set.all():
            dnsmasq.append('-G')
            dnsmasq.append('%s,%s' % (str(lease.mac), str(lease.address)))

        system.call(dnsmasq, netns=network.netns_name, background=True)

        network.set_prop('dhcp_running', True)
        network.save()


    def stop_dhcp(self, task):
        network = task.get_obj('Subnet')

        try:
            dnsmasq_procs = [int(x) for x in subprocess.check_output(['pgrep', 'dnsmasq']).splitlines()]
            ns_procs = [int(x) for x in subprocess.check_output(['sudo', 'ip', 'netns', 'pids', network.netns_name]).splitlines()]

            for pid in ns_procs:
                if pid in dnsmasq_procs:
                    try:
                        #os.kill(pid, 15)
                        subprocess.call(['sudo', 'ip', 'netns', 'exec', network.netns_name, 'kill', '-15', str(pid)])
                    except:
                        pass
        except Exception, e:
            syslog(msg="Failed to kill DHCP process: " + str(e))

        network.set_prop('dhcp_running', False)
        network.save()
