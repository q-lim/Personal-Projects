"""
Console App for Sample Tracker
Records laboratory samples
Version 2: GUI version
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from SampleTracker import SampleManager, SolidSample, LiquidSample



def create_sample(manager, parent):
    """Sample creation"""

    form = tk.Toplevel(parent)
    form.title("Add Sample")
    form.geometry("450x500")

    # Make popup behave like modal dialog
    form.transient(parent)
    form.grab_set()

    # -------------------------
    # Variables
    # -------------------------
    sample_type_var = tk.StringVar()

    # -------------------------
    # Sample Type Dropdown
    # -------------------------
    tk.Label(form, text="Sample Type").grid(row=0, column=0, padx=10, pady=5)

    sample_type_menu = ttk.Combobox(
        form,
        textvariable=sample_type_var,
        values=["Solid", "Liquid"],
        state="readonly"
    )
    sample_type_menu.grid(row=0, column=1)

    # Common Fields
    def add_label_entry(frame, text, row):
        tk.Label(frame, text=text).grid(row=row, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=row, column=1)
        return entry

    tk.Label(form, text="Name").grid(row=1, column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=1, column=1)

    tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
    date_entry = tk.Entry(form)
    date_entry.grid(row=2, column=1)

    tk.Label(form, text="Experiment Number").grid(row=3, column=0)
    exp_entry = tk.Entry(form)
    exp_entry.grid(row=3, column=1)

    tk.Label(form, text="Lab Location").grid(row=4, column=0)
    lab_entry = tk.Entry(form)
    lab_entry.grid(row=4, column=1)

    tk.Label(form, text="Storage Location").grid(row=5, column=0)
    stor_entry = tk.Entry(form)
    stor_entry.grid(row=5, column=1)


    # Solid Frame
    solid_frame = tk.Frame(form)
    stor_med_entry = add_label_entry(solid_frame, "Storage Medium", 0)
    stor_med_vol_entry = add_label_entry(solid_frame, "Medium Volume", 1)
    sample_mass_entry = add_label_entry(solid_frame, "Sample Mass", 2)

    # Liquid Frame
    liquid_frame = tk.Frame(form)
    bottle_entry = add_label_entry(liquid_frame, "Bottle Type", 0)
    bottle_vol_entry = add_label_entry(liquid_frame, "Bottle Volume", 1)
    sample_vol_entry = add_label_entry(liquid_frame, "Sample Volume", 2)


    def update_fields(event=None):
        """Dynamic field display"""

        solid_frame.grid_forget()
        liquid_frame.grid_forget()

        if sample_type_var.get() == "Solid":
            solid_frame.grid(row=6, column=0, columnspan=2, pady=10)

        elif sample_type_var.get() == "Liquid":
            liquid_frame.grid(row=6, column=0, columnspan=2, pady=10)

    sample_type_menu.bind("<<ComboboxSelected>>", update_fields)


    def clear_fields():
        """Clear fields"""

        name_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        exp_entry.delete(0, tk.END)
        lab_entry.delete(0, tk.END)
        stor_entry.delete(0, tk.END)

        stor_med_entry.delete(0, tk.END)
        stor_med_vol_entry.delete(0, tk.END)
        sample_mass_entry.delete(0, tk.END)

        bottle_entry.delete(0, tk.END)
        bottle_vol_entry.delete(0, tk.END)
        sample_vol_entry.delete(0, tk.END)


    def submit_sample():
        """Submit sample"""

        try:
            name = name_entry.get()
            date = date_entry.get()
            exp = exp_entry.get()
            lab = lab_entry.get()
            stor = stor_entry.get()

            if not name or not date or not exp:
                messagebox.showwarning(
                    "Missing Data",
                    "Please fill Name, Date, and Experiment Number",
                    parent=form
                )
                return

            if sample_type_var.get() == "Solid":

                sample = SolidSample(
                    name,
                    date,
                    exp,
                    lab,
                    stor,
                    stor_med_entry.get(),
                    stor_med_vol_entry.get(),
                    sample_mass_entry.get()
                )

            elif sample_type_var.get() == "Liquid":

                sample = LiquidSample(
                    name,
                    date,
                    exp,
                    lab,
                    stor,
                    bottle_entry.get(),
                    bottle_vol_entry.get(),
                    sample_vol_entry.get()
                )

            else:
                messagebox.showerror(
                    "Error",
                    "Select sample type",
                    parent=form
                )
                return

            manager.add_sample(sample)

            messagebox.showinfo(
                "Success",
                "Sample added successfully",
                parent=form
            )

            clear_fields()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=form
            )


    # Buttons
    tk.Button(
        form,
        text="Add Sample",
        width=15,
        command=submit_sample
    ).grid(row=7, column=0, pady=20)

    tk.Button(
        form,
        text="Exit",
        width=15,
        command=form.destroy
    ).grid(row=7, column=1)



def list_samples(manager, parent):
    """Lists out all samples recorded"""

    samples = manager.list_samples()

    if not samples:
        messagebox.showinfo("Samples", "No samples found", parent=parent)
        return

    text = ""

    for s in samples:
        text += f"{s.ID}\n{s.Name}\n{s.Status}\n----------\n"

    messagebox.showinfo("Samples", text, parent=parent)



def update_sample_status(manager, parent):
    """Updates status of a sample"""

    sample_id = simpledialog.askstring(
        "Update Status",
        "Enter Sample ID",
        parent=parent
    )

    if not sample_id:
        return

    sample = manager.find_sample(sample_id)

    if not sample:
        messagebox.showerror("Error", "Sample not found", parent=parent)
        return

    status = simpledialog.askstring(
        "Status",
        "Enter new status",
        parent=parent
    )

    if status:
        sample.update_status(status)
        manager.save_samples()



def delete_sample(manager, parent):
    """Deletes a sample"""

    sample_id = simpledialog.askstring(
        "Delete Sample",
        "Enter Sample ID",
        parent=parent
    )

    if sample_id:
        manager.delete_sample(sample_id)



def main():

    manager = SampleManager()

    root = tk.Tk()
    root.title("Sample Logger")
    root.geometry("450x500")

    tk.Label(
        root,
        text="Sample Logger",
        font=("Arial", 16)
    ).pack(pady=20)

    tk.Button(
        root,
        text="Add Sample",
        width=25,
        command=lambda: create_sample(manager, root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="List Samples",
        width=25,
        command=lambda: list_samples(manager, root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Update Status",
        width=25,
        command=lambda: update_sample_status(manager, root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Delete Sample",
        width=25,
        command=lambda: delete_sample(manager, root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Exit",
        width=25,
        command=root.destroy
    ).pack(pady=20)

    root.mainloop()



if __name__ == "__main__":
    main()