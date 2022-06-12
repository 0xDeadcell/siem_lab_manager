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

    key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\VMware, Inc.\\VMware Workstation\\OVFTool')
    reg.SetValueEx(key, 'InstallPath', 0, reg.REG_SZ, 'C:\\"Program Files (x86)\\VMware\\VMware Workstation\\OVFTool\\ovftool.exe"')
    reg.CloseKey(key)
    from pyvmrun import PyVmrun


def compress_vm_files(path, target_running, recursive=False):
    import subprocess
    valid_vmx_paths = [path for path in list_running_vms()]
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=path, recursive=recursive)

    # Stops all valid VMXs files in the list
    for current_path in valid_vmx_paths:
        print(f"\n[*] Checking if VM at {current_path} is currently running...")
        if pathlib.Path(current_path).stem in str(list_running_vms()):
            print(f"[!] {pathlib.Path(current_path).stem} is currently running, attempting to stop now...")
            stop_vms(vmx_paths=path, target_running=target_running, recursive=recursive)
        print(f"[+] Attempting to compress {pathlib.Path(current_path).stem} to 7z with LZMA2 max compression.")
        
        # Compression of files
        os.system(f"cd {os.path.split(current_path)[0]}")


        valid_vm_extensions = ['.vmx', '.vmdk', '.vmxf', '.nvram', '.vmsd']

        valid_vm_files = [os.path.join(os.path.split(current_path)[0], f) for f in os.listdir(os.path.split(current_path)[0]) if os.path.splitext(f)[-1] in valid_vm_extensions]
        #for i in valid_vm_files:
            #print(f"Attempting to compress '{pathlib.Path(i).name}' into '{pathlib.Path(current_path).stem}.7z'")
        #print("")
        joined_files = '"' + '" "'.join(valid_vm_files) + '"'
        command = [r'C:\\"Program Files\\7-Zip\\7z.exe"', 'a', '-t7z', '-m0=lzma2', '-mx=9', '-aoa', '-y', '"' + os.path.join(os.path.split(current_path)[0], str(pathlib.Path(current_path).stem)) + '.7z' + '"', joined_files]
        print("CMD: " + ' '.join(command))
        
        os.system(' '.join(command))
        print(f"Created 7z archive at {os.path.join(os.path.split(current_path)[0], str(pathlib.Path(current_path).stem)) + '.7z'}")


def download_homelab(path, dest_path):
    gauth = GoogleAuth()
    gdrive = GoogleDrive(gauth)
    # Download the VMs
    # https://drive.google.com/file/d/1OgjI4Bw9K4py4eLz2IKz0RzOPzX-RvRH/view?usp=sharing
    gdd.download_file_from_google_drive(file_id="https://drive.google.com/file/d/" + path + "?confirm=1", dest_path=dest_path, unzip=True, showsize=True)


def convert_vmx_to_ova(path, target_running, recursive=False):
    import winreg as reg
    key = reg.OpenKeyEx(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\VMware, Inc.\\VMware Workstation\\OVFTool')
    value = reg.QueryValueEx(key, 'InstallPath')[0]
    if key:
        reg.CloseKey(key)

    valid_vmx_paths = [path for path in list_running_vms()]
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=path, recursive=recursive)

    # Stops all valid VMXs files in the list
    for current_path in valid_vmx_paths:
        print(f"\n[*] Checking if VM at {current_path} is currently running...")
        if pathlib.Path(current_path).stem in str(list_running_vms()):
            print(f"[!] {pathlib.Path(current_path).stem} is currently running, attempting to stop now...")
            stop_vms(vmx_paths=path, target_running=target_running, recursive=recursive)
        print(f"[+] Attempting to convert {pathlib.Path(current_path).name} to OVA format.")
        print(f'[*] CMD: {value} --overwrite --compress=9 --noImageFiles --skipManifestCheck --targetType=OVA "{current_path}" "{os.path.splitext(current_path)[0]}.ova"\n')
        os.system(fr'{value} --overwrite --compress=9 --noImageFiles --skipManifestCheck --targetType=OVA "{current_path}" "{os.path.splitext(current_path)[0]}.ova"')


def get_valid_vmxs(path, recursive=False):
    # Recursive
    valid_vmx_paths = []
    if recursive:
        valid_vmx_paths = [os.path.join(root, f) for root, dirs, files in os.walk(path) for f in files if os.path.splitext(f)[1] in [".vmx"] ]
    else:
        valid_vmx_paths = [ pathlib.Path.joinpath(path, f) for f in os.listdir(path) if os.path.splitext(f)[1] in [".vmx"] ] 
    return valid_vmx_paths


def start_vms(vmx_paths, recursive=False):
    # Gets a list of all valid VMX files starting from the top of the path
    valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)

    # Starts all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        # Start the VM
        print(f"[+] Starting VM at {current_vmx_path}")
        vm.start()


def stop_vms(vmx_paths, target_running, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]
    # Stops all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        
        print(f"[+] Attempting to stop VM at {current_vmx_path}")
        # Stop the VM
        vm.stop(mode='soft')
        

def suspend_vms(vmx_paths, target_running, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]
    # Suspends all valid VMXs files in the list
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)
        print(f"[+] Attempting to suspend VM at {current_vmx_path}")
        # Suspend the VM
        vm.suspend()


def delete_vms(vmx_paths, target_running, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Deletes all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to delete VM at {current_vmx_path}")
        # Delete the VM
        vm.deleteVM()


def create_snapshot(vmx_paths, target_running, snapshot_name, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Creates a snapshot for all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to create snapshot {snapshot_name} for VM at {current_vmx_path}")
        # Create the snapshot
        vm.snapshot(name=snapshot_name)
        


def delete_snapshot(vmx_paths, target_running, snapshot_name, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Deletes a snapshot for all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to delete snapshot {snapshot_name} for VM at {current_vmx_path}")
        # Delete the snapshot
        vm.deleteSnapshot(name=snapshot_name)


def restore_snapshot(vmx_paths, target_running, snapshot_name, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
    else:
        valid_vmx_paths = [path for path in list_running_vms()]

    # Restores from a snapshot in all valid VMs in the list using the VMX files
    for current_vmx_path in valid_vmx_paths:
        vm = PyVmrun(current_vmx_path)

        print(f"[+] Attempting to restore a snapshot for VM at {current_vmx_path}")
        # Restore the snapshot
        vm.revertToSnapshot(name=snapshot_name)


def list_snapshots(vmx_paths, target_running, recursive=False):
    if not target_running:
        # Gets a list of all valid VMX files starting from the top of the path
        valid_vmx_paths = get_valid_vmxs(path=vmx_paths, recursive=recursive)
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
    running_vms = list(vm.list().keys())
    if len(running_vms) == 0:
        print("[*] No running VMs found")
    return running_vms


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and control a homelab all from the comfort of your terminal.')
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    group = parser.add_mutually_exclusive_group(required=True)
   
    parser.add_argument("-d", "--vm_directory_path", help="The path where your VMs are/will be stored.", default=os.getcwd(), type=pathlib.Path)
    
    exclusive_group.add_argument("-t", "--target_running", help="Set all other commands to target only running VMs", action="store_true")
    exclusive_group.add_argument("-r", "--recursive", help="Set the search for VMXs to be recursive from the specified directory", action="store_true")

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
    group.add_argument("--convert_to_ova", help="Attempt to stop a VM, and convert it to OVA format", action="store_true")
    group.add_argument('-c', '--compress', help="Compress the VM files with LZMA2 compression", action="store_true")
    args = parser.parse_args()

    if args.target_running:
        print("[*] Tool search mode set to target only running VMs")
    else:
        print(f"[*] Tool search directory set to {args.vm_directory_path}")

    if args.recursive:
        print("[*] Tool search mode set to recursive")

    if args.start_vms:
        start_vms(vmx_paths=args.vm_directory_path, recursive=args.recursive)

    if args.delete_vms:
        stop_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)
        delete_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)
    
    if args.stop_vms:
        stop_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)

    if args.suspend_vms:
        suspend_vms(vmx_paths=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)

    if args.list_running_vms:
        running_vms = sorted(list_running_vms())
        print(f"[+] Currently {len(running_vms)} VMs are running")
        for i in running_vms:
            print(i)

    if args.compress:
        compress_vm_files(path=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)

    if args.convert_to_ova:
        convert_vmx_to_ova(path=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)

    if args.list_snapshots:
        list_snapshots(vmx_paths=args.vm_directory_path, target_running=args.target_running, recursive=args.recursive)

    if args.create_snapshot:
        create_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.create_snapshot, recursive=args.recursive)
    
    if args.restore_snapshot:
        restore_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.restore_snapshot, recursive=args.recursive)

    if args.delete_snapshot:
        delete_snapshot(vmx_paths=args.vm_directory_path, target_running=args.target_running, snapshot_name=args.delete_snapshot, recursive=args.recursive)

    #if args.download_homelab:
    #    path = pathlib.Path(args.vm_directory_path)
    #    if not path.is_dir():
    #        print(f"[+] Downloading homelab to {args.vm_directory_path} now...")
    #        download_homelab(path=args.download_homelab, dest_path=args.vm_directory_path)
    #    else:
    #        print("[!] Invalid Path - Please specify a filename...")