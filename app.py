import customtkinter as ctk
import subprocess
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Remote Support Toolkit")
app.geometry("800x600")

def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )
        output_box.delete("1.0", "end")
        output_box.insert("end", result.stdout or result.stderr)
    except Exception as e:
        output_box.delete("1.0", "end")
        output_box.insert("end", f"Error: {e}")

def ping_host():
    host = input_box.get()
    run_command(f"ping {host}")

def dns_lookup():
    host = input_box.get()
    run_command(f"nslookup {host}")

def ip_config():
    run_command("ipconfig /all")

def flush_dns():
    run_command("ipconfig /flushdns")

def system_info():
    run_command("systeminfo")

def test_port():
    host = input_box.get()
    port = port_box.get()

    if not host or not port:
        output_box.delete("1.0", "end")
        output_box.insert("end", "Enter both host and port.")
        return

    command = f"powershell Test-NetConnection {host} -Port {port}"
    run_command(command)

def save_log():
    content = output_box.get("1.0", "end")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/support_log_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(content)

    output_box.insert("end", f"\n\nSaved log to {filename}")

title = ctk.CTkLabel(app, text="Remote Support Toolkit", font=("Arial", 28))
title.pack(pady=20)

input_box = ctk.CTkEntry(app, placeholder_text="Enter hostname, IP, or website", width=400)
input_box.pack(pady=10)

port_box = ctk.CTkEntry(app, placeholder_text="Enter port, example: 443", width=400)
port_box.pack(pady=10)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

ctk.CTkButton(button_frame, text="Ping Host", command=ping_host).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(button_frame, text="DNS Lookup", command=dns_lookup).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(button_frame, text="IP Config", command=ip_config).grid(row=0, column=2, padx=10, pady=10)

ctk.CTkButton(button_frame, text="Flush DNS", command=flush_dns).grid(row=1, column=0, padx=10, pady=10)
ctk.CTkButton(button_frame, text="Test Port", command=test_port).grid(row=1, column=1, padx=10, pady=10)
ctk.CTkButton(button_frame, text="System Info", command=system_info).grid(row=1, column=2, padx=10, pady=10)

ctk.CTkButton(app, text="Save Output to Log", command=save_log).pack(pady=10)

output_box = ctk.CTkTextbox(app, width=720, height=250)
output_box.pack(pady=20)

app.mainloop()