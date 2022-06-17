# Lab Contents

## Network Map

<p align="center"><img src="/images/homelab_apps.png?raw=true"/></p>


## Overview of VMs, running services, and some of the installed applications

### Lab Dashboard (vm_dashboard)
- Homer
- Opencti
- MITRE Caldera: ready to deploy to hosts (must be started in portainer first)
- TheHive
- Portainer
- WikiJS

<p align="center"><img src="/images/dashboard.png?raw=true"/></p>
<p align="center"><img src="/images/caldera.png?raw=true"/></p>

### Network Kit (vm_network_kit)
- Elasticsearch
- Kibana - 
 **NOTE**: In order to allow logs to flow, the following 3 indexes must be deleted:
	winlogbeat-7.17.0, filebeat-7.16.3, arkime_sessions3
	To delete these indexes -> Kibana (192.168.100.13:5601) -> Hamburger Menu -> Stack Management -> Index Management -> Select the 3 indexes and delete them)
- Jupyter Notebooks
- Zeek
- Redmine
- Mattermost
- Arkime
- Ghosts Server and Grafana Dashboard

<p align="center"><img src="/images/kibana.png?raw=true"/></p>
 
### Domain Controller (vm_dc2019)
- DNS Configured
- GPO Policies setup
- Sysmon deployed
- Winlogbeats deployed
- Ghosts (NPC/Traffic generation tool): ready to deploy
- BadBlood: ready to deploy

### Exchange Server (vm_exchange2016)
- OWA webmail/ecp setup: mail.vulnlab.com

<p align="center"><img src="/images/mail.png?raw=true"/></p>

### pfSense Router (vm_pfsense)
- KitNetwork (OPT1)
- Vulnlab Network (LAN)
- FakeNetwork (WAN)

### Flare (vm_flare)
- Default Flare tools setup on Desktop
- Atomic Red Team Tools added

<p align="center"><img src="/images/flarevm.png?raw=true"/></p>


### Win10 Enterprise 1 (vm_win10_01)
- Sysmon deployed
- Winlogbeats deployed
- Ghosts (NPC/Traffic generation tool): ready to deploy
- Atomic Red Team Tools added
- OWASP JuiceShop running

<p align="center"><img src="/images/juiceshop.png?raw=true"/></p>


### OWASP Broken Web Application Security Project (VM_BWAP)
- List of running applications/sites can be found on the (Google OWASP Wiki)[https://code.google.com/archive/p/owaspbwa/wikis/UserGuide.wiki]

<p align="center"><img src="/images/owasp_bwa.png?raw=true"/></p>


## Video Walkthrough of the lab
- Will eventually add a Youtube video here


## Additions to the lab
If you have any suggestion or would like to add a VM from your lab to this project, then please [create an issue](https://github.com/0xDeadcell/manage_homelab/issues/new) before starting a new pull request.