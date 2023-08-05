Installation:
1. Install python package via PIP:
    pip install coredhcp

2. Enable API module in /etc/corecluster/config.py file:
    LOAD_API = [...
                'coredhcp.views.api']

3. Enable coredhcp hook in /etc/corecluster/config.py file:
    HOOK_PIPELINES = {
        ...
        'network.delete.prepare': ['coredhcp.hooks.network'],
    }

4. Enable CoreDHCP agent in /etc/corecluster/agent.py file:
    AGENTS = [
        ...
        {'type': 'dhcp', 'module': 'coredhcp.agents.dhcp', 'count': 1}
    ]
