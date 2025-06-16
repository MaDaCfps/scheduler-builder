import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Add this line
import csv
import json

def generate_schedule():
    schedule = assign_schedule()
    with open("schedule_output.csv", "w", newline="") as csvfile:
        fieldnames = ["date", "staff", "shift", "start", "end"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, entries in schedule.items():
            for entry in entries:
                writer.writerow({
                    "date": date,
                    "staff": entry["staff"],
                    "shift": entry["shift"],
                    "start": entry["start"],
                    "end": entry["end"]
                })
    messagebox.showinfo("Done", "Schedule generated successfully!")

def edit_staff():
    def save_staff():
        name = name_entry.get()
        max_hours = max_hours_entry.get()

        if not name or not max_hours.isdigit():
            messagebox.showerror("Error", "Please enter a name and number of hours.")
            return

        try:
            with open("data/staff.json", "r") as f:
                staff_list = json.load(f)
        except:
            staff_list = []

        new_staff = {
            "name": name,
            "seniority": 1,
            "max_hours": int(max_hours),
            "availability": {},
            "time_off": []
        }

        staff_list.append(new_staff)
        with open("data/staff.json", "w") as f:
            json.dump(staff_list, f, indent=2)

        messagebox.showinfo("Saved", f"{name} added!")
        popup.destroy()

    # Popup window
    popup = tk.Toplevel(root)
    popup.title("Add Staff")
    popup.geometry("300x180")

    # Labels + ttk.Entry fields
    tk.Label(popup, text="Staff Name:").pack(pady=(10, 0))
    name_entry = ttk.Entry(popup)
    name_entry.pack(pady=5)

    tk.Label(popup, text="Max Weekly Hours:").pack()
    max_hours_entry = ttk.Entry(popup)
    max_hours_entry.pack(pady=5)

    # Save button
    tk.Button(popup, text="Save", command=save_staff).pack(pady=10)

    # Create popup window
    popup = tk.Toplevel(root)
    popup.title("Add Staff")
    popup.geometry("300x180")
    popup.configure(bg="#f2f2f2")

    tk.Label(popup, text="Staff Name:", bg="#f2f2f2", fg="black").pack(pady=(10, 0))
    name_entry = tk.Entry(popup, bg="white", fg="black")
    name_entry.pack(pady=5)

    tk.Label(popup, text="Max Weekly Hours:", bg="#f2f2f2", fg="black").pack()
    max_hours_entry = tk.Entry(popup, bg="white", fg="black")
    max_hours_entry.pack(pady=5)

    tk.Button(popup, text="Save", command=save_staff).pack(pady=10)

# --- Main Window ---
root = tk.Tk()
root.title("Scheduler Builder")
root.geometry("400x300")

tk.Label(root, text="Scheduler Builder", font=("Helvetica", 16)).pack(pady=20)
tk.Button(root, text="Generate Schedule", command=generate_schedule).pack(pady=10)
tk.Button(root, text="Add Staff", command=edit_staff).pack(pady=10)

root.mainloop()
