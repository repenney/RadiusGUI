import tkinter as tk
from tkinter import ttk, messagebox
from config import SYSTEMS_CLUSTERS





class ClusterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Select System and Cluster", font=('Segoe UI', 16, 'bold')).pack(pady=(10, 20))

       
        # System dropdown
        self.system_var = tk.StringVar()
        self.system_dropdown = ttk.Combobox(self, textvariable=self.system_var, state="readonly")
        self.system_dropdown['values'] = list(SYSTEMS_CLUSTERS.keys())
        self.system_dropdown.bind("<<ComboboxSelected>>", self.update_clusters)
        self.system_dropdown.pack(pady=10)

        # Cluster dropdown
        self.cluster_var = tk.StringVar()
        self.cluster_dropdown = ttk.Combobox(self, textvariable=self.cluster_var, state="readonly")
        self.cluster_dropdown.pack(pady=10)


        # Navigation Buttons
        ttk.Button(self, text="Next", command=self.next_page).pack(pady=(10, 5))

    def update_clusters(self, event=None):
        selected_system = self.system_var.get()
        clusters = SYSTEMS_CLUSTERS.get(selected_system, [])
        self.cluster_dropdown['values'] = clusters
        self.cluster_var.set('')  # Clear previous selection

    def next_page(self):
        system = self.system_var.get()
        cluster = self.cluster_var.get()

        if not system or not cluster:
            messagebox.showwarning("Input Error", "Please select both a system and a cluster.")
            return

        # Save selections to controller
        self.controller.selected_system = system
        self.controller.selected_cluster = cluster

    
        # Move to the next page
        self.controller.show_frame("SetupPage")
