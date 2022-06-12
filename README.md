
# MANAGE_HOMELAB.py

Automate tedious VMware functions for your homelab with ease

## TODO List

- [x] Add conversion to OVA format
- [ ] Add an upload/download feature to/from Google Drive
- [ ] Add an option to output the IP address and the VMnet Interface
- [ ] Generate a Network Map based off the IP addresses, VMnet Interfaces and OS of Guests

## Installation Steps

Clone the project

```bash
git clone https://github.com/0xDeadcell/manage_homelab.git
```

Go to the project directory

```bash
cd manage_homelab
```

Install the required python modules

```bash
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python manage_homelab.py -h


usage: manage_homelab.py [-h] [-d VM_DIRECTORY_PATH] [-t | -r]
                         (--delete_vms | --start_vms | --stop_vms | --suspend_vms | --create_snapshot CREATE_SNAPSHOT | --restore_snapshot RESTORE_SNAPSHOT | --delete_snapshot DELETE_SNAPSHOT | --list_snapshots | -l | --convert_to_ova)

Download and control a homelab all from the comfort of your terminal.

options:
  -h, --help            show this help message and exit
  -d VM_DIRECTORY_PATH, --vm_directory_path VM_DIRECTORY_PATH
                        The path where your VMs are/will be stored.
  -t, --target_running  Set all other commands to target only running VMs
  -r, --recursive       Set the search for VMXs to be recursive from the specified directory
  --delete_vms          Delete the targeted VMs
  --start_vms           Start the targeted VMs
  --stop_vms            Stop the targeted VMs
  --suspend_vms         Suspend the targeted VMs
  --create_snapshot CREATE_SNAPSHOT
                        Create a snapshot for all targeted VMs, requires a snapshot name
  --restore_snapshot RESTORE_SNAPSHOT
                        Attempt to restore a snapshot for all targeted VMs, requires a snapshot name
  --delete_snapshot DELETE_SNAPSHOT
                        Attempt to delete a snapshot for all targeted VMs, requires a snapshot name
  --list_snapshots      Output a list of snapshots for all targeted VMs
  -l, --list_running_vms
                        List all running VMs
  --convert_to_ova      Attempt to stop a VM, and convert it to OVA format
```

## Demo
<p align="center"><img src="/images/render_compressed.gif?raw=true"/></p>
