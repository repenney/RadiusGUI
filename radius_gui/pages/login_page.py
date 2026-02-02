import tkinter as tk
from tkinter import messagebox, ttk
from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import SubscriptionClient
from env_loader import required
import os
from utils.vm_manager import azure_cli_login


# This page handles the Azure login process using the InteractiveBrowserCredential
# from the Azure Identity library. It allows users to authenticate via a web browser.
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        # Title label
        ttk.Label(self, text="Login to Ameriband Azure", font=("Segoe UI", 16)).pack(pady=30)

        # Login button
        login_button = ttk.Button(self, text="Login with Azure", command=self.login_with_azure)
        login_button.pack(pady=10)

    def login_with_azure(self):
        try:
            # Trigger browser-based Azure login
            tenant_id = required("TENANT_ID") 
            credential = InteractiveBrowserCredential(tenant_id=tenant_id)

            # Validate login by attempting to list subscriptions
            subs_client = SubscriptionClient(credential)
            list(subs_client.subscriptions.list())  # triggers login

            # Save the credential to the app for later use
            self.controller.user_azure_token = credential
        
            if not azure_cli_login():
                raise Exception(messagebox.showerror("Azure CLI", "Login failed."))
    
            # Move to the next page
            self.controller.show_frame("ClusterPage")

        except Exception as e:
            messagebox.showerror("Login Failed", f"Azure login failed:\n{e}")

