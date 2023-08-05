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

from corecluster.utils import validation as v
from corecluster.utils.decorators import register
from corecluster.utils.exception import CoreException
from corecluster.cache.task import Task
from corecluster.models.core import Subnet


@register(auth='token', validate={'network_id': v.is_id(),
                                  'gateway_ip': v.is_string()})
def start(context, network_id, gateway_ip):
    """
    Start DHCP server(s) in isolated network.
    :param network_id: Isolated network, which should be connected with new VPN server
    :param gateway_ip: Gateway ip for isolated network.
    """

    network = Subnet.get(context.user_id, network_id)
    if network.network_pool.mode != 'isolated':
        raise CoreException('network_not_isolated')

    network.set_prop('gateway', gateway_ip)
    network.save()

    if network.get_prop('dhcp_running', False):
        task = Task()
        task.type = 'dhcp'
        task.action = 'stop_dhcp'
        task.append_to([network], broadcast=True)

    task = Task()
    task.type = 'dhcp'
    task.action = 'start_dhcp'
    task.append_to([network])


@register(auth='token', validate={'network_id': v.is_id()})
def stop(context, network_id):
    """
    Stop DHCP servers in network
    """
    network = Subnet.get(context.user_id, network_id)
    if network.network_pool.mode != 'isolated':
        raise CoreException('network_not_isolated')

    task = Task()
    task.type = 'dhcp'
    task.action = 'stop_dhcp'
    task.append_to([network], broadcast=True)
