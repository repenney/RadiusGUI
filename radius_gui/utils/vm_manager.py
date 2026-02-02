from tkinter import messagebox
import paramiko
from io import StringIO
from utils.secrets import get_ssh_key_from_keyvault
from config import VMS, RESOURCE_GROUPS
import subprocess
import json



'''
This module contains functions to manage VM operations for setting up a Radius instance.
It accesses every VM on the associated cluster, and configures the new Radius instance.
'''
def execute_instance_setup(keyvault_name, secret_name, vms, username, instance, auth_port, acct_port, shared_secret, overlay=None):
    # Fetch SSH key and prepare
    private_key_str = get_ssh_key_from_keyvault(keyvault_name, secret_name)
    key = paramiko.RSAKey.from_private_key(StringIO(private_key_str))

    commands = [
        ("Copying template...", f"sudo cp -ar /etc/freeradius/sites-available/merakitemplate /etc/freeradius/sites-available/{instance}"),
        ("Entering operator name...", f"sudo sed -i 's/testsite/{instance}/g' /etc/freeradius/sites-available/{instance}"),
        ("Entering auth port...", f"sudo sed -i 's/99998/{auth_port}/g' /etc/freeradius/sites-available/{instance}"),
        ("Entering acct port...", f"sudo sed -i 's/99999/{acct_port}/g' /etc/freeradius/sites-available/{instance}"),
        ("Entering shared secret...", f"sudo sed -i 's/supersecret/{shared_secret}/g' /etc/freeradius/sites-available/{instance}"),
        ("Creating symbolic link...", f"sudo ln -s /etc/freeradius/sites-available/{instance} /etc/freeradius/sites-enabled/{instance}"),
        ("Updating permissions...", f"sudo chown -R freerad:freerad /etc/freeradius/sites-enabled/{instance}"),
        ("Restarting freeradius service...", f"sudo systemctl restart freeradius")
    ]

    rollback_commands = [
        f"sudo rm /etc/freeradius/sites-enabled/{instance}",
        f"sudo rm /etc/freeradius/sites-available/{instance}",
        f"sudo systemctl restart freeradius"
    ]

    exists_command = f'''[ -f /etc/freeradius/sites-available/{instance} ] && echo "True" || echo "False"'''  # Check if operator name is already used


    hosts_completed = []
    hosts_progress = {}

    if overlay:
        overlay.update_title("Setting Up Radius Instances…")

    for host in vms:
        try:
            if overlay:
                overlay.after(0, overlay.reset_steps, 0, None)
                overlay.after(0, overlay.update_title, f"Running setup on {host}")


            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=username, pkey=key)
            

            hosts_progress[host] = 0
            hosts_completed.append(host)


            # Check if operator name is already used
            stdin, stdout, stderr = client.exec_command(exists_command)  
            exists = stdout.read().decode().strip()
            if exists == "True":
                if overlay:
                    overlay.after(0, lambda: messagebox.showerror("Operator Name Exists", f"Operator name '{instance}' already exists on {host}."))
                    overlay.after(0, overlay.finish, False)
                client.close()
                return False
            

            #Connection successful
            if overlay:
                overlay.after(0, overlay.update_step, 0, True)  


            #Run set up commands
            for i, (desc, cmd) in enumerate(commands):
                if overlay:
                    overlay.after(0, overlay.update_step, i+1, True)

                stdin, stdout, stderr = client.exec_command(cmd)
                out = stdout.read().decode().strip()
                err = stderr.read().decode().strip()
                output = out + "\n" + err if out or err else ""

                hosts_progress[host] = i + 1    #mark progress in case of rollback

                if output:
                    if overlay:
                        overlay.after(0, overlay.update_step, i+1, False)  # mark this step ❌
                    raise Exception(f"Command failed on {host}:\n{output}")

                if overlay:
                    overlay.after(0, overlay.update_step, i+1, True)

            # After finishing all commands on this host
            if overlay:
                overlay.after(0, overlay.finish, True)

            client.close()


        except Exception as e:
            # Rollback only on hosts that had some setup
            for completed_host in hosts_completed:
                if hosts_progress.get(completed_host, 0) > 0:
                    try:
                        client.connect(hostname=completed_host, username=username, pkey=key)
                        for cmd in rollback_commands[:hosts_progress[completed_host]]:
                            #print(f"Rolling back on {completed_host}: {cmd}")
                            stdin, stdout, stderr = client.exec_command(cmd)
                        client.close()
                    except Exception as rollback_error:
                        if overlay:
                            overlay.after(0, overlay.update_step, False)
                            messagebox.showerror(
                                f"Rollback failed on {completed_host}: {rollback_error}\n\n{e}"
                            )
                            overlay.after(0, overlay.destroy)
                            #print(f"Rollback failed on {completed_host}: {rollback_error}")

            if overlay:
                overlay.after(0, lambda msg=str(e): messagebox.showerror(
                    "Setup Failed",
                    f"SSH connection or command failed.\nAll changes on previously connected hosts were rolled back.\n\nDetails:\n{msg}"
                ))
                overlay.after(0, overlay.destroy)

            return False

    return True



'''
This function retrieves the port numbers for authentication and accounting
by checking the highest 4-digit UDP port currently in use on the specified VM.
'''
def get_port_numbers(system, cluster, keyvault_name, secret_name, username):
    """
    Accesses the necessary VM configuration to determine the ports for authentication and accounting.
    """
    
    try:
        private_key_str = get_ssh_key_from_keyvault(keyvault_name, secret_name)

        key = paramiko.RSAKey.from_private_key(StringIO(private_key_str))

    except Exception as e:
        messagebox.showerror(
            title="SSH Key Error",
            message=f"Failed to retrieve SSH key from Key Vault.\n\nError Details:\n{e}"
        )
        return None

    vm = VMS[system][cluster][0]

    # This command finds the highest 4-digit UDP port currently in use, which we will use as a base for our new ports.
    port_command = '''ss -tulpn | awk '$1 == "udp" && $2 == "UNCONN" {split($5, a, ":"); if (a[2] ~ /^[0-9]{4}$/) print a[2]}' | sort -n | tail -n 1'''
    
    try:

        #print(f"Connecting to {vm}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=vm, username=username, pkey=key)

        
        #print(f"Executing on {vm}: {port_command}")
        stdinn, stdout, stderr = client.exec_command(port_command)

        # Read the output and store it in a variable
        ref_port = int(stdout.read().decode().strip())

        # Print the result (optional)
        #print("The last 4-digit port is:", ref_port)


        client.close()

        #print(f"Completed setup on {vm}.\n")
    except Exception as e:
        messagebox.showerror(
            title="Connection Failed",
            message=f"Failed to connect to Host {vm}.\nCheck VPN connection.\n\nError Details:\n{e}"
        )
        return None

    # Generate new ports based on the reference port
    auth_port = ref_port + 1
    acct_port = ref_port + 2


    return str(auth_port), str(acct_port)



'''
This function retrieves the next available priority for a new NSG rule.
'''
def get_next_priority(nsg_name, resource_group):
    """
    This function retrieves the next available priority for a new NSG rule.
    It assumes priorities are in the range 100-4096 and increments by 100.
    """
    az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
    
    cmd = [
        az_path, "network", "nsg", "rule", "list",
        "--nsg-name", nsg_name,
        "--resource-group", resource_group,
        "--output", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    rules = json.loads(result.stdout)

    # Extract existing 3-digit priorities (100–999)
    priorities = [
        rule.get("priority") for rule in rules
        if isinstance(rule.get("priority"), int) and 100 <= rule["priority"] < 1000
    ]

    if not priorities:
        return 100  # Start at 100 if no rules exist

    next_priority = max(priorities) + 1
    
    return next_priority




'''
This function creates port rules in the Azure firewall for the specified system and cluster.
It adds NSG rules to allow traffic on the specified authentication and accounting ports.
'''
def create_port_rules(system, name, auth_port, acct_port, overlay=None):

    port1 = int(auth_port)
    port2 = int(acct_port)  
    az_path = "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
                  

    if overlay:
        overlay.update_title("Creating NSG Firewall Rules…")


    for resource_group, nsg_name in RESOURCE_GROUPS[system]:
        
        if overlay:
                overlay.after(0, overlay.reset_steps, 0, None)
                overlay.after(0, overlay.update_title, f"Adding NSG rule for {resource_group} / {nsg_name}...")

        #Get next priority
        try:
            if overlay:
                overlay.after(0, overlay.update_step, 0, True)

            priority = str(get_next_priority(nsg_name, resource_group))


        except Exception as e:
            if overlay:
                overlay.after(0, overlay.update_step, 0, False)
                messagebox.showerror(
                    "NSG Setup Error",
                    f"An error occurred while retrieving next priority for NSG rules.\n"
                    f"Please configure Azure nsg manually.\n\n{e}"
                )
                overlay.after(0, overlay.destroy)
        
        try:
            if overlay:
                overlay.after(0, overlay.update_step, 1, True)

            create_rule_cmd = [
                az_path,
                "network", "nsg", "rule", "create",
                "--resource-group", resource_group,
                "--nsg-name", nsg_name,
                "--name", name,
                "--protocol", "UDP",
                "--direction", "Inbound",
                "--priority", priority,
                "--access", "Allow",
                "--source-port-ranges", "*",
                "--destination-port-ranges", f"{port1}-{port2}"
            ]

            result = subprocess.run(create_rule_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode != 0:
                if overlay:
                    overlay.after(0, overlay.update_step, 1, False)
                
                raise Exception(f"Failed to create NSG rule:\n{result.stderr}")

            if overlay:
                overlay.after(0, overlay.finish, True)
            #print(f"NSG rule '{name}' added")

        except Exception as e:
            if overlay:
                overlay.after(0, overlay.update_step, False)
                messagebox.showerror(
                    "NSG Setup Error",
                    f"An error occurred while creating NSG rules.\n"
                    f"Please verify rules in Azure manually.\n\n{e}"
                )
                overlay.after(0, overlay.destroy)

            return False



'''
Check if Azure CLI is logged in, and if not pop up window for them to login at.
'''
def azure_cli_login():
    AZ_PATH = r"C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd"
    try:
        # Run 'az account show' to check if already logged in
        result = subprocess.run(
            [AZ_PATH, "account", "show"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.returncode != 0:
            # Not logged in, prompt user to login
            messagebox.showinfo("Azure Login", "Please login to Azure CLI in the popup window.")
            subprocess.run([AZ_PATH, "login"])
        
            # Optional: confirm login
            result = subprocess.run([AZ_PATH, "account", "show"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                messagebox.showinfo("Azure Login", "Successfully logged in!")
            else:
                messagebox.showerror("Azure Login", "Login failed. Please try again.")
        
    except Exception as e:
        messagebox.showerror("Azure Login", f"An error occurred:\n{e}")
        return False

    return True

