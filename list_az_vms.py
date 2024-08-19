import subprocess
import json
import sys

def check_azure_cli_installed():
    """Check if Azure CLI is installed."""
    try:
        subprocess.run(['az', '--version'], check=True, text=True, capture_output=True)
        print("Azure CLI is installed.")
    except FileNotFoundError:
        print("Azure CLI is not installed. Please install Azure CLI to proceed.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Azure CLI is installed but could not run `az --version`. Please ensure it's correctly configured.")
        sys.exit(1)

def check_azure_cli_logged_in():
    """Check if Azure CLI is logged in."""
    try:
        result = subprocess.run(['az', 'account', 'show'], check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print("Azure CLI is logged in.")
        else:
            print("Azure CLI is not logged in. Please log in using `az login`.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Azure CLI is not logged in. Please log in using `az login`.")
        sys.exit(1)

def get_active_vms():
    """Fetch and display active Azure Virtual Machines in all regions."""
    try:
        result = subprocess.run(
            ['az', 'vm', 'list', '--query', "[].{ID:id, Name:name, Type:type, Location:location}"],
            check=True,
            text=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Azure CLI command: {e}")
        return []

    vms = json.loads(result.stdout)

    if not vms:
        print("No active VMs found.")
        return

    # Print VM details including their locations
    for vm in vms:
        vm_id = vm.get('ID')
        vm_name = vm.get('Name')
        vm_type = vm.get('Type')
        vm_location = vm.get('Location')
        print(f"ID: {vm_id}")
        print(f"Name: {vm_name}")
        print(f"Type: {vm_type}")
        print(f"Location: {vm_location}")
        print('-' * 40)

def main():
    check_azure_cli_installed()
    check_azure_cli_logged_in()
    
    get_active_vms()

if __name__ == "__main__":
    main()
