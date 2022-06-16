import os
import sys
import argparse
import pathlib
import subprocess


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


def get_zip_path():
    if sys.platform == "win32":
        # Windows
        zip_path = r'C:\\"Program Files\\7-Zip\\7z.exe"'
    else:
        # Unix
        zip_path = subprocess.check_output(['which', '7z']).decode('utf-8').strip()
        if zip_path == '':
            sys.exit("[!] Please install the 7zip package and try running again!")
    return zip_path


def compress_vm_files(path, target_running, recursive=False):
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
        zip_path = get_zip_path()
        command = [zip_path, 'a', '-t7z', '-m0=lzma2', '-mx=9', '-aoa', '-y', '"' + os.path.join(os.path.split(current_path)[0], str(pathlib.Path(current_path).stem)) + '.7z' + '"', joined_files]
        print("CMD: " + ' '.join(command))
        
        os.system(' '.join(command))
        print(f"Created 7z archive at {os.path.join(os.path.split(current_path)[0], str(pathlib.Path(current_path).stem)) + '.7z'}")


def extract_vm(zip_file, dest_path, prompt):
    zip_path = get_zip_path()
    
    if not prompt:
        overwrite = '-aos'
        prompt = '-y'
    else:
        overwrite = ''
        prompt = ''
    try:
        os.chdir(dest_path)
        os.mkdir(pathlib.Path(zip_file).stem)
        os.chdir(os.path.join(dest_path, pathlib.Path(zip_file).stem))
    except Exception as e:
        print(e)
    print(f"[+] Extracting {zip_file} into {os.getcwd()} now...")
    # Force extract to destination, autorename the output file if the zip output already exists
    command = [zip_path, 'x', zip_file, '-o' + '"' + os.path.join(os.getcwd(), pathlib.Path(zip_file).stem) + '"', overwrite, prompt]
    print(' '.join(command))
    os.system(' '.join(command))


def download_homelab(lab_file, dest_path, extract=False):
    abs_path_lab_file = os.path.join(os.getcwd(), lab_file)
    # Download the VMs
    # https://drive.google.com/file/d/1OgjI4Bw9K4py4eLz2IKz0RzOPzX-RvRH/view?usp=sharing
    if sys.platform == "win32":
        # Windows
        # So we can download the file in the temp directory
        os.chdir(os.environ['temp'])
        gd_downloader = os.path.join(os.getcwd(), 'goodls_windows_amd64.exe')
        if not 'goodls_windows_amd64.exe' in os.listdir():
            # Only download the Google Drive downloader if it doesn't already exist
            command = ['curl', '-L', 'https://github.com/tanaikech/goodls/releases/download/v2.0.1/goodls_windows_amd64.exe', '-o', 'goodls_windows_amd64.exe']
            # Execute the command to retrieve the google drive downloader
            print(f"Retrieving google drive downloader tool, and placing it in temp.")
            os.system(' '.join(command))
    else:
        os.chdir('/tmp')
        gd_downloader = os.path.join(os.getcwd(), 'goodls_linux_amd64')
        # sys.exit('[!] Please chmod +x /tmp/goodls_linux_amd64 before running again')
        if not 'goodls_linux_amd64' in os.listdir():
            #if subprocess.check_output(['chmod', '-u']).decode('utf-8').strip() != '0':
                #sys.exit("[!] Please re-run your command with sudo")

            # Only download the Google Drive downloader if it doesn't already exist
            command = ['wget', 'https://github.com/tanaikech/goodls/releases/download/v2.0.1/goodls_linux_amd64']
            # Execute the command to retrieve the google drive downloader
            print(f"Retrieving google drive downloader tool, and placing it in temp.")
            os.system(' '.join(command))
            subprocess.call(['chmod', '+x', '/tmp/goodls_linux_amd64'])
    print(f"Downloading VMs into {dest_path} with links from {abs_path_lab_file}")
    
    os.chdir(dest_path)
    download_lab_command = [gd_downloader, ' < ', abs_path_lab_file]
    os.system(' '.join(download_lab_command))
    if extract:
        print(f"[*] Extract flag set, attempting to unzip all 7z files in {dest_path}")
        zip_files = [i for i in os.listdir() if i.endswith('7z')]
        print(zip_files)
        for zip_file in zip_files:
            extract_vm(zip_file=zip_file, dest_path=dest_path, prompt=False)


def convert_vmx_to_ova(path, target_running, recursive=False):
    if sys.platform == "win32":
        # Windows w/ vmware tools installed
        import winreg as reg
        key = reg.OpenKeyEx(reg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\VMware, Inc.\\VMware Workstation\\OVFTool')
        vmrun = reg.QueryValueEx(key, 'InstallPath')[0]
        
        if key:
            reg.CloseKey(key)
    else:
        # Unix w/ vmware tools installed
        try:
            vmrun = subprocess.check_output(['which', 'vmrun']).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            sys.exit("[!] Please ensure that vmrun is install and try running again!")

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
        print(f'[*] CMD: {vmrun} --overwrite --compress=9 --noImageFiles --skipManifestCheck --targetType=OVA "{current_path}" "{os.path.splitext(current_path)[0]}.ova"\n')
        os.system(fr'{vmrun} --overwrite --compress=9 --noImageFiles --skipManifestCheck --targetType=OVA "{current_path}" "{os.path.splitext(current_path)[0]}.ova"')


def get_valid_vmxs(path, recursive=False):
    # Recursive
    valid_vmx_paths = []
    if recursive:
        valid_vmx_paths = [os.path.join(root, f) for root, dirs, files in os.walk(path) for f in files if os.path.splitext(f)[1] in [".vmx"] ]
    else:
        valid_vmx_paths = [ os.path.join(path, f) for f in os.listdir(path) if os.path.splitext(f)[1] in [".vmx"] ] 
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
    return running_vms


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and control a homelab all from the comfort of your terminal.')
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    group = parser.add_mutually_exclusive_group(required=False)
   
    parser.add_argument("-d", "--vm_directory_path", help="The path where your VMs are/will be stored.", default=os.getcwd(), type=pathlib.Path)
    parser.add_argument('-x', '--extract', help="Extract 7z file(s) from a current or specified directory, when used with --download_homelab VM(s) will be extracted automatically", default=False, action="store_true")
    exclusive_group.add_argument("-t", "--target_running", help="Set all other commands to target only running VMs", action="store_true")
    exclusive_group.add_argument("-r", "--recursive", help="Set the search for VMXs to be recursive from the specified directory", action="store_true")
    
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
    group.add_argument("--download_homelab", help="Download one or more VMs from a shared Google Drive by specifying a file containing one or multiple shared links. Used with -d", action="store", type=pathlib.Path)
    
    args = parser.parse_args()

    args.vm_directory_path = os.path.abspath(os.path.join(os.getcwd(), args.vm_directory_path))

    # If no arguments, print help
    if len(sys.argv) < 2:
        sys.exit(parser.print_help())

    if args.target_running:
        print("[*] Tool search mode set to target only running VMs")
    else:
        print(f"[*] Tool search directory set to {args.vm_directory_path}")

    if args.recursive:
        print("[*] Tool search mode set to recursive")

    if len(list_running_vms()) == 0:
        print("[*] No running VMs found")

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

    if args.download_homelab:
        if args.extract:
            print("[+] Extract flag is set, will automatically attempt to extract downloaded VMs")
        else:
            print("[-] Extract flag is not set, please run with -x if you'd like VMs extracted after download completion")
        path = pathlib.Path(args.download_homelab)
        dest_path = pathlib.Path(args.vm_directory_path)
        if not path.is_file():
            sys.exit("[!] Please specify a valid file containing Google Drive links")
        elif not dest_path.is_dir():
            sys.exit("[!] Please specify a valid directory path to store the VM(s) in with -d")
        elif path.is_file():
            print(f"[+] Downloading VMs to {args.vm_directory_path} now...")
            download_homelab(lab_file=args.download_homelab, dest_path=args.vm_directory_path, extract=args.extract)

    if args.extract:
        print(f"[*] Checking {args.vm_directory_path} for *.7z files to extract")
        zip_files = [ '"' + os.path.join(args.vm_directory_path, i) + '"' for i in os.listdir(args.vm_directory_path) if i.endswith('7z')]
        print("[+] Found files to extract, will prompt if overwriting is needed: ")
        for i in zip_files:
            print(i)
        for zip_file in zip_files:
            extract_vm(zip_file=zip_file,dest_path=args.vm_directory_path, prompt=True)
    
