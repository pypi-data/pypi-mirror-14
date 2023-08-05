"""
Copyright (c) 2016 Marta Nabozny

This file is part of CoreCluster project.

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

from corenetwork.network_mixin import NetworkMixin
from corenetwork.os_mixin import OsMixin
from corenetwork.api_mixin import ApiMixin
from corenetwork.config_mixin import ConfigMixin
from corenetwork.hook_interface import HookInterface
from corecluster.utils.logger import *
import subprocess


class Hook(NetworkMixin, OsMixin, ApiMixin, ConfigMixin, HookInterface):
    task = None

    def start(self):
        super(Hook, self).finish()
        network = self.task.get_obj('Subnet')

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
