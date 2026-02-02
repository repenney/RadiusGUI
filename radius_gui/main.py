import tkinter as tk
from tkinter import ttk
from pages.login_page import LoginPage
from pages.cluster_page import ClusterPage
from pages.setup_page import SetupPage
from pages.result_page import ResultPage



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ameriband Radius Instance Setup")
        self.geometry("510x400")
        self.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Segoe UI', 11))
        self.style.configure('TEntry', font=('Segoe UI', 11))
        self.style.configure('TButton', font=('Segoe UI', 12), padding=6)
        self.style.configure('TCombobox', font=('Segoe UI', 11))

        self.container = ttk.Frame(self, padding=15)
        self.container.pack(fill="both", expand=True)

        # Frame dictionary with string keys
        self.frames = {}    

        # Register all pages
        for F in (LoginPage, ClusterPage, SetupPage, ResultPage):
            page_name = F.__name__  # e.g., "LoginPage"
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.user_azure_token = None
        self.selected_cluster = None
        self.instance_data = {}

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
