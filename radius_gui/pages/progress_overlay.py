import tkinter as tk


class ProgressOverlay(tk.Toplevel):
    def __init__(self, parent, steps, size):
        super().__init__(parent)
        self.title("Setup Progress")
        self.geometry(size)
        self.configure(bg="white")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Add this line — the dynamic title label
        self.title_label = tk.Label(self, text="", font=("Segoe UI", 14, "bold"), bg="white")
        self.title_label.pack(pady=10)

        self.step_labels = []
        self.steps = steps
        self.current_step = 0

        for step in steps:
            frame = tk.Frame(self, bg="white")
            frame.pack(anchor="w", padx=10, pady=5, fill="x")
            icon = tk.Label(frame, text="⬜", font=("Arial", 14), bg="white")
            icon.pack(side="left")
            label = tk.Label(frame, text=step, font=("Arial", 12), bg="white", anchor="w")
            label.pack(side="left", padx=10, fill="x", expand=True)
            self.step_labels.append((icon, label))

    def update_step(self, step_index, success=True):
        # Mark the previous step ✅ or ❌
        if step_index > 0:
            prev_icon, _ = self.step_labels[step_index - 1]
            prev_icon.config(text="✅" if success else "❌")

        # Show ⏳ on the current step
        if step_index < len(self.step_labels):
            current_icon, _ = self.step_labels[step_index]
            current_icon.config(text="⏳")
            self.current_step = step_index

    def reset_steps(self, *args):
        _ = args
        for icon, _ in self.step_labels:
            icon.config(text="⬜")
        self.current_step = 0


    def update_title(self, title):
        self.title_label.config(text=title)
    
    def finish(self, success):
        # Final step icon: ✅ or ❌
        icon, _ = self.step_labels[self.current_step]
        icon.config(text="✅" if success else "❌")

        # Optionally mark all remaining steps as ❌ if failed early
        if not success:
            for i in range(self.current_step + 1, len(self.step_labels)):
                icon, _ = self.step_labels[i]
                icon.config(text="❌")
        

        #self.after(2500, self.destroy)




