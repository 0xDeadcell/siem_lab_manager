
# MANAGE_HOMELAB.py

Automate tedious VMware functions for your homelab with ease on either Windows or Linux hosts, or simply install a Pre-built lab.


### Pre-built Cybersecurity VULNLAB
For an already built lab please check out my [Cybersecurity VULNLAB](/lab_contents.md) for an extensive look at the VMs, pre-configured applications and a list of running services.
Install instructions for this **optional** lab are below.



## TODO List

- [x] Add conversion to OVA format
- [x] Add the option to compress VM files with LZMA2
- [x] Add a feature to download VMs from Google Drive
- [x] Add a feature to extract zipped (*.7z) VMs
- [ ] Add multi-threading for VM download operations
- [ ] Add an option to output the IP address and the VMnet Interface
- [ ] Generate a Network Map based off the IP addresses, VMnet Interfaces and OS of Guests

## Known Issues
1. Certain Linux VMs won't power off with the stop command:

    Solutions:
    - Option 1: Stop the VM manually
    - Option 2: Change the line where it says: vm.stop(mode='soft') to vm.stop(mode='hard') 


2. Some VMs aren't being downloaded, or an error saying 'invalid url' is appearing 

    Details: When downloading a VM through Google Drive (by specifying `--download_homelab prebuilt_labs\recommended_lab_links.txt`), rate limiting may occur if a file has been downloaded more than a certain amount within 24 hours.

    Solutions:
    - Option 1: Run your command with `--download_homelab_onedrive prebuilt_labs\onedrive_recommended_lab_links.txt` option, this will attempt to download the lab via OneDrive instead of Google Drive which has less severe rate limiting
    - Option 2: Wait a few hours and try again (you can remove links from recommended_lab_links.txt that have already been downloaded)
    - Option 3: Please reach out to me, and I'll share a direct link to the VM(s) with you


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

## **Optional** Download and start a homelab from Google Drive

If you don't have the time to setup a lab, then check out my [Cybersecurity VULNLAB](/lab_contents.md) or continue below for how to install it.


### Install a Cybersecurity VULNLAB
```bash
python3 manage_homelab.py --download_homelab_onedrive prebuilt_labs\onedrive_recommended_lab_links.txt -d ..\path\to\vm\directory -x
python3 manage_homelab.py --create_snapshot baseline_snapshot -d ..\path\to\vm\directory
python3 manage_homelab.py --start_vms -d ..\path\to\vms\directory
```


## Usage

```bash
python manage_homelab.py -h


usage: manage_homelab.py [-h] [-d VM_DIRECTORY_PATH] [-x] [-t | -r]
                         [--delete_vms | --start_vms | --stop_vms | --suspend_vms | --create_snapshot SNAPSHOT_NAME | --restore_snapshot SNAPSHOT_NAME | --delete_snapshot SNAPSHOT_NAME | --list_snapshots | -l | --convert_to_ova | -c | --download_homelab FILENAME.TXT | --download_homelab_onedrive FILENAME.TXT]

Download and control a homelab all from the comfort of your terminal.

options:
  -h, --help            show this help message and exit
  -d VM_DIRECTORY_PATH, --vm_directory_path VM_DIRECTORY_PATH
                        The path where your VMs are/will be stored.
  -x, --extract         Extract 7z file(s) from a current or specified directory, when used with --download_homelab VM(s) will be extracted automatically
  -t, --target_running  Set all other commands to target only running VMs
  -r, --recursive       Set the search for VMXs to be recursive from the specified directory
  --delete_vms          Delete the targeted VMs
  --start_vms           Start the targeted VMs
  --stop_vms            Stop the targeted VMs
  --suspend_vms         Suspend the targeted VMs
  --create_snapshot SNAPSHOT_NAME
                        Create a snapshot for all targeted VMs, requires a snapshot name
  --restore_snapshot SNAPSHOT_NAME
                        Attempt to restore a snapshot for all targeted VMs, requires a snapshot name
  --delete_snapshot SNAPSHOT_NAME
                        Attempt to delete a snapshot for all targeted VMs, requires a snapshot name
  --list_snapshots      Output a list of snapshots for all targeted VMs
  -l, --list_running_vms
                        List all running VMs
  --convert_to_ova      Attempt to stop a VM, and convert it to OVA format
  -c, --compress        Compress the VM files with LZMA2 compression
  --download_homelab FILENAME.TXT
                        Download one or more VMs from a shared Google Drive by specifying a file containing one or multiple shared links. Used with -d
  --download_homelab_onedrive FILENAME.TXT
                        Download one or more VMs from a shared OneDrive by specifying a file containing one or multiple shared links. Used with -d
```

## Demo
<p align="center"><img src="/images/render_compressed.gif?raw=true"/></p>
