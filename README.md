
# MANAGE_HOMELAB.py

Automate tedious VMware functions for your homelab with ease


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
pip install requirements.txt
```

## Usage

```bash
python manage_homelab.py -h


usage: manage_homelab.py [-h] [-d VM_DIRECTORY_PATH] [-t]
                         (--delete_vms | --start_vms | --stop_vms | --suspend_vms | --create_snapshot CREATE_SNAPSHOT | --restore_snapshot RESTORE_SNAPSHOT | --delete_snapshot DELETE_SNAPSHOT | --list_snapshots | -l)

Download and control a homelab all from the comfort of your terminal.

options:
  -h, --help            show this help message and exit
  -d VM_DIRECTORY_PATH, --vm_directory_path VM_DIRECTORY_PATH
                        The path where your VMs are/will be stored.
  -t, --target-running  Set all other commands to target only running VMs
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
```

