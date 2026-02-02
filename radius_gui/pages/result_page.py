import tkinter as tk
from tkinter import ttk
from config import SYSTEM_IPS




class ResultPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        

        # Title with dynamic instance name
        self.title_var = tk.StringVar()
        self.title_label = ttk.Label(self, textvariable=self.title_var, font=('Segoe UI', 14, 'bold'))
        self.title_label.pack(pady=(10, 5))

        # Display system and cluster
        self.info_label = ttk.Label(self, text="", font=('Segoe UI', 11, 'italic'))
        self.info_label.pack(pady=(0, 15))

        # Results display box
        self.result_text = tk.Text(
            self,
            width=60,
            height=10,
            font=('Consolas', 11),
            state="disabled",
            bg="#f7f7f7",
            relief="flat",
            bd=1
        )
        self.result_text.pack(pady=(0, 15))

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Create Another", command=self.create_another).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.controller.destroy).grid(row=0, column=2, padx=5)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.display_result()

    def display_result(self):
        data = self.controller.instance_data

        # Set dynamic title with instance name
        operator_name = data.get("operator_name", "Unknown")
        title_text = f"Radius Instance Created for {operator_name}"
        self.title_var.set(title_text)

        # Dynamically resize window if text is too long
        if len(title_text) > 50:  # adjust this threshold if needed
            new_width = 800  # or calculate based on len(title_text)
            self.controller.geometry(f"{new_width}x500")
    

        system = getattr(self.controller, 'selected_system', 'Unknown System')
        cluster = getattr(self.controller, 'selected_cluster', 'Unknown Cluster')


        fqdn_e, ip_e = SYSTEM_IPS.get(system, {}).get('east', ("Unknown FQDN", "Unknown IP"))
        fqdn_w, ip_w = SYSTEM_IPS.get(system, {}).get('west', ("Unknown FQDN", "Unknown IP"))

        self.info_label.config(text=f"System: {system}    •    Cluster: {cluster}")

        output = (
            f"{operator_name}\n"
            f"{fqdn_e} ({ip_e})\n"
            f"{fqdn_w} ({ip_w})\n\n"
            f"authentication: udp/{data['auth_port']}\n"
            f"accounting:    udp/{data['acct_port']}\n\n"
            f"key: {data['shared_secret']}\n"
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, output)
        self.result_text.config(state="disabled")

        self.latest_output = output


    def copy_to_clipboard(self):
        import tkinter as tk
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.latest_output)
        r.update()
        r.destroy()

    def create_another(self):
        self.controller.show_frame("ClusterPage")
