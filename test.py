import tkinter as tk
from tkinter import messagebox, ttk
import paramiko


def save_changes():
    new_values = [f"{key}={value.get()}" for key, value in entries.items()]
    new_content = '\n'.join(new_values)

    try:
        # Create a SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        # Write new content to the remote file
        with ssh.open_sftp().file(remote_env_file_path, 'w') as f:
            f.write(new_content)

        ssh.close()
        messagebox.showinfo('Success', 'Changes saved!')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')


hostname = "192.168.20.124"
username = "op"
password = "opopop"
remote_env_file_path = "/home/op/compose/env"

# Load existing key-value pairs from remote env file
entries = {}
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    with ssh.open_sftp().file(remote_env_file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            entries[key] = value

    ssh.close()
except Exception as e:
    print(f'An error occurred: {str(e)}')

# Create GUI window
window = tk.Tk()
window.title("Remote Environment Variable Editor")
window.geometry("600x600")  # Set the initial window size

# Create and place widgets
frame = ttk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

row = 0
for key, value in entries.items():
    key_label = tk.Label(inner_frame, text=key)
    key_label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

    value_entry = tk.Entry(inner_frame)
    value_entry.insert(0, value)
    value_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

    entries[key] = value_entry
    row += 1

save_button = tk.Button(inner_frame, text="Save Changes", command=save_changes)
save_button.grid(row=row, columnspan=2, pady=10)

# Start GUI event loop
window.mainloop()
