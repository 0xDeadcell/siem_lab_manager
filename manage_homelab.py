import os
import sys
import argparse
import pathlib
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive

# patch PyVmrun so it finds the vmrun path in the registry
try:
    from pyvmrun import PyVmrun
except FileNotFoundError:
    import winreg as reg
    print("[+] Setting VMRUN path in registry for first run...")
    key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\VMware, Inc.\\VMware Workstation')
    reg.SetValueEx(key, 'InstallPath', 0, reg.REG_SZ, '"C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrun.exe"')
    reg.CloseKey(key)
    from pyvmrun import PyVmrun


def download_homelab(path, dest_path):
    gauth = GoogleAuth()
    gdrive = GoogleDrive(gauth)
    # Download the VMs
    # https://drive.google.com/file/d/1OgjI4Bw9K4py4eLz2IKz0RzOPzX-RvRH/view?usp=sharing
    gdd.download_file_from_google_drive(file_id="https://drive.google.com/file/d/" + path + "?confirm=1", dest_path=dest_path, unzip=True, showsize=True)


def get_valid_vmxs(path):
    valid_vmx_paths = [ pathlib.Path.joinpath(path, f) for f in os.listdir(path) if os.path.splitext(f)[1] in [".vmx"] ] 
    return valid_vmx_paths


def start_vms(vmx_paths):
    # Gets a list of all valid VMX files starting from the top of the path
    valid_vmx_paths = get_valid_vmxs(path=vmx_paths)

    # Starts all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        # Start the VM
        print(f"[+] Starting VM at {current_vmx_path}")
        vm.start()


def stop_vms(vmx_paths, target_running):
    
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]
    # Stops all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        print(f"[+] Stopping VM at {current_vmx_path}")
        # Stop the VM
        vm.stop()
        

def suspend_vms(vmx_paths, target_running):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]
    # Suspends all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        # Suspend the VM
        print(f"[+] Suspending VM at {current_vmx_path}")
        vm.suspend()


def delete_vms(vmx_paths, target_running):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Deletes all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Delete VM at {current_vmx_path}")
        # Delete the VM
        vm.deleteVM()


def create_snapshot(vmx_paths, target_running, snapshot_name):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Creates a snapshot for all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to create snapshot {snapshot_name} for VM at {current_vmx_path}")
        # Create the snapshot
        vm.snapshot(name=snapshot_name)


def delete_snapshot(vmx_paths, target_running, snapshot_name):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Deletes a snapshot for all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Delete snapshot {snapshot_name} for VM at {current_vmx_path}")
        # Delete the snapshot
        vm.deleteSnapshot(name=snapshot_name)


def restore_snapshot(vmx_paths, target_running, snapshot_name):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Restores from a snapshot in all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to restore a snapshot for VM at {current_vmx_path}")
        # Restore the snapshot
        vm.revertToSnapshot(name=snapshot_name)


def list_snapshots(vmx_paths, target_running):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Restores from a snapshot in all valid VMs in the list using the VMX files

    all_snapshots = []
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"\n[+] Checking for snapshots for VM at {current_vmx_path}")
        # Return a List of the snapshot
        current_snapshot = vm.listSnapshots()
        all_snapshots.append(current_snapshot)
        for snapshot in current_snapshot:
            print(snapshot, end='')

    return all_snapshots

def list_running_vms():
    vm = PyVmrun(vmx="")
    return list(vm.list().keys())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and control a homelab all from the comfort of your terminal.')
    group = parser.add_mutually_exclusive_group(required=True)
        #group.add_argument("-d", "--vm_directory_path", help="The path where your VMs are/will be stored.", nargs=1, type=pathlib.Path)
    #group.add_argument("-t", "--target-running", help="Set all other commands to target only running VMs", action="store_true")
    parser.add_argument("-d", "--vm_directory_path", help="The path where your VMs are/will be stored.", default=os.getcwd(), type=pathlib.Path)
    parser.add_argument("-t", "--target-running", help="Set all other commands to target only running VMs", action="store_true")

    #group.add_argument("--download_homelab", help="Google Drive sharing ID to homelab (e.g., 1OgjI4Bw9K4py4eLz2IKz0RzOPzX-RvRH)", action="store")
    group.add_argument("--delete_vms", help="Delete the targeted VMs", action="store_true")
    group.add_argument("--start_vms", help="Start the targeted VMs", action="store_true")
    group.add_argument("--stop_vms", help="Stop the targeted VMs", action="store_true")
    group.add_argument("--suspend_vms", help="Suspend the targeted VMs", action="store_true")
    group.add_argument("--create_snapshot", help="Create a snapshot for all targeted VMs, requires a snapshot name", type=str)
    group.add_argument("--restore_snapshot", help="Attempt to restore a snapshot for all targeted VMs, requires a snapshot name", type=str)
    group.add_argument("--delete_snapshot", help="Attempt to delete a snapshot for all targeted VMs, requires a snapshot name", type=str)
    group.add_argument("--list_snapshots", help="Output a list of snapshots for all targeted VMs", action="store_true")
    group.add_argument("-l", "--list_running_vms", help="List all running VMs", action="store_true")
    args = parser.parse_args()


    if args.start_vms:
        start_vms(vmx_paths=args.vm_directory_path)

    if args.delete_vms:
        stop_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running)
        delete_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running)
    
    if args.stop_vms:
        stop_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running)

    if args.suspend_vms:
        suspend_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running)

    if args.list_running_vms:
        running_vms = sorted(list_running_vms())
        print(f"[+] Currently {len(running_vms)} VMs are running")
        for i in running_vms:
            print(i)

    if args.list_snapshots:
        list_snapshots(vmx_paths=args.vm_directory_path, target_running=args.target_running)

    if args.create_snapshot:
        create_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.create_snapshot)
    
    if args.restore_snapshot:
        restore_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.restore_snapshot)

    if args.delete_snapshot:
        delete_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.delete_snapshot)

    #if args.download_homelab:
    #    path = pathlib.Path(args.vm_directory_path)
    #    if not path.is_dir():
    #        print(f"[+] Downloading homelab to {args.vm_directory_path} now...")
    #        download_homelab(path=args.download_homelab, dest_path=args.vm_directory_path)
    #    else:
    #        print("[!] Invalid Path - Please specify a filename...")