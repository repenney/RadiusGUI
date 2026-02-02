import tkinter as tk
from tkinter import ttk
import random
from utils.vm_manager import execute_instance_setup, get_port_numbers, create_port_rules
from config import VMS, KEYS
from pages.progress_overlay import ProgressOverlay
import string
from threading import Thread




class SetupPage(ttk.Frame):

    #Determines the look of the page
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Make this frame expand vertically inside the container
        self.pack_propagate(False)
        self.grid_rowconfigure(99, weight=1)  # let last row grow

        ttk.Label(self, text="Create New Radius Instance", font=('Segoe UI', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Display selected system and cluster at the top
        self.info_label = ttk.Label(self, text="", font=('Segoe UI', 12))
        self.info_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Instance Name
        ttk.Label(self, text="Operator Name:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.entry_instance = ttk.Entry(self, width=35)
        self.entry_instance.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

        # Authentication Port
        ttk.Label(self, text="Authentication Port:").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.auth_port_var = tk.StringVar()
        self.auth_port_entry = ttk.Entry(self, width=10, textvariable=self.auth_port_var)
        self.auth_port_entry.grid(row=5, column=0, pady=5, padx=5)

        # Accounting Port
        ttk.Label(self, text="Accounting Port:").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.acct_port_var = tk.StringVar()
        self.acct_port_entry = ttk.Entry(self, width=10, textvariable=self.acct_port_var)
        self.acct_port_entry.grid(row=7, column=0, pady=5, padx=5)

        ttk.Button(self, text="Submit", command=self.submit).grid(row=8, column=1, pady=20, padx=5)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("ClusterPage")).grid(row=8, column=0, pady=20, padx=5)

        # This spacer row will take all extra vertical space pushing content up, adding bottom margin
        spacer = ttk.Frame(self)
        spacer.grid(row=99, column=0, columnspan=2, sticky='nswe')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(99, weight=1)  # spacer grows to fill bottom space


    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)

        # Update system and cluster info label on page raise
        system = getattr(self.controller, 'selected_system', 'Unknown System')
        cluster = getattr(self.controller, 'selected_cluster', 'Unknown Cluster')
        self.info_label.config(text=f"Selected System: {system}    Selected Cluster: {cluster}")

        keyvault_name, secret_name = KEYS[system][cluster]

        # Generate next available ports
        ports = get_port_numbers(
            system=system,
            cluster=cluster,
            keyvault_name=keyvault_name,
            secret_name=secret_name,
            username="appuser"
        )

        if ports is None:
            self.controller.show_frame("ClusterPage")
            return

        auth_port = ports[0]
        acct_port = ports[1]
        self.auth_port_var.set(auth_port)
        self.acct_port_var.set(acct_port)



    # generate_key function to create a random shared secret
    # This function generates a random string of letters and digits
    def generate_key(self, length=32):
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k=length))



    def submit(self):
        operator = self.entry_instance.get().strip()
        if not operator:
            tk.messagebox.showwarning("Input Error", "Please enter an operator name")
            return

        accounting_port = self.acct_port_var.get()
        authentication_port = self.auth_port_var.get()
        secret = self.generate_key()

        system = getattr(self.controller, 'selected_system', 'Unknown System')
        cluster = getattr(self.controller, 'selected_cluster', 'Unknown Cluster')
        keyvault_name, secret_name = KEYS[system][cluster]

        self.controller.instance_data = {
            "operator_name": operator,
            "system": system,
            "cluster": cluster,
            "auth_port": authentication_port,
            "acct_port": accounting_port,
            "shared_secret": secret
        }

        params = {
            "keyvault_name": keyvault_name,
            "secret_name": secret_name,
            "vms": VMS[system][cluster],
            "username": "appuser",
            "instance": operator,
            "auth_port": authentication_port,
            "acct_port": accounting_port,
            "shared_secret": secret
        }

        steps = [
            "Connecting to VM...",
            "Copying template...",
            "Entering operator name...",
            "Entering auth port...",
            "Entering acct port...",
            "Entering shared secret...",
            "Creating symbolic link...",
            "Updating permissions...",
            "Finishing setup..."
        ]


        self.overlay = ProgressOverlay(self, steps, size="500x400")
        Thread(target=self.run_setup_process, args=(params,), daemon=True).start()


    def run_setup_process(self, params,):
        try:
            #run the instance setup process with overlay
            success = execute_instance_setup(**params, overlay=self.overlay)
            self.overlay.after(1000, self.overlay.destroy)
            
            nsg_steps = [
                "Getting next available priority for NSG rules...",
                f"Creating NSG rule for ports {params['auth_port']}-{params['acct_port']}..."
            ]

            def on_complete():
                #Close the instance setup overlay

                #If the instance setup was successful, save the system IPs and operator name for the result page
                #Then, create the NSG rules
                if success:
                    system = getattr(self.controller, 'selected_system', 'Unknown System')
                    operator = self.entry_instance.get().strip()
                    

                    def run_nsg_creation():
                        try:
                            self.nsg_overlay = ProgressOverlay(self, nsg_steps, size="800x250")
                            create_port_rules(
                                system, 
                                operator, 
                                params["auth_port"], 
                                params["acct_port"],
                                overlay=self.nsg_overlay
                            )
                            
                            # Safely finish overlay and show results page on main thread
                            self.nsg_overlay.after(0, lambda: (
                                self.nsg_overlay.after(1000, self.nsg_overlay.destroy),
                                self.controller.show_frame("ResultPage")
                            ))

                             
                        except Exception as e:
                            print(f"Error creating port rules: {e}")
                            self.nsg_overlay.after(0, lambda: self.nsg_overlay.finish(False))
                            self.controller.show_frame("ResultPage")


                    #Run NSG creation in a separate thread
                    Thread(target=run_nsg_creation, daemon=True).start()


            self.overlay.after(0, on_complete)

        except Exception as e:
            print(f"Error: {e}")
            self.overlay.after(0, lambda: self.overlay.finish(False))
            




















