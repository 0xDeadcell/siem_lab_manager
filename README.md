
# MANAGE_HOMELAB.py

Automate tedious VMware functions for your homelab with ease

## TODO List

- [x] Add conversion to OVA format
- [x] Add the option to compress VM files with LZMA2
- [x] Add a feature to download VMs from Google Drive
- [x] Add a feature to extract zipped (*.7z) VMs
- [ ] Add an option to output the IP address and the VMnet Interface
- [ ] Generate a Network Map based off the IP addresses, VMnet Interfaces and OS of Guests

## Known Issues
Certain Linux VMs won't power off with the stop command:

Solutions:
- Stop the VM manually
OR
- Change the line where it says: vm.stop(mode='soft') to vm.stop(mode='hard') 

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

## Download and start a homelab from Google Drive

```bash
python3 manage_homelab.py --download_homelab example_vm_link.txt -d ..\path\to\vm\directory -x
python3 manage_homelab.py --create_snapshot baseline_snapshot -d ..\path\to\vm\directory
python3 manage_homelab.py --start_vms -d ..\path\to\vms\directory
```


## Usage

```bash
python manage_homelab.py -h


usage: manage_homelab.py [-h] [-d VM_DIRECTORY_PATH] [-x] [-t | -r]
                         [--delete_vms | --start_vms | --stop_vms | --suspend_vms | --create_snapshot CREATE_SNAPSHOT | --restore_snapshot RESTORE_SNAPSHOT | --delete_snapshot DELETE_SNAPSHOT | --list_snapshots | -l | --convert_to_ova | -c | --download_homelab DOWNLOAD_HOMELAB]

Download and control a homelab all from the comfort of your terminal.

options:
  -h, --help            show this help message and exit
  -d VM_DIRECTORY_PATH, --vm_directory_path VM_DIRECTORY_PATH
                        The path where your VMs are/will be stored.
  -x, --extract         Extract 7z file(s) from a current or specified directory, when used with --download_homelab
                        VM(s) will be extracted automatically
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
  -c, --compress        Compress the VM files with LZMA2 compression
  --download_homelab DOWNLOAD_HOMELAB
                        Download one or more VMs from a shared Google Drive by specifying a file containing one or
                        multiple shared links. Used with -d
```

## Demo
<p align="center"><img src="/images/render_compressed.gif?raw=true"/></p>
