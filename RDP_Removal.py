import tkinter as tk
import os
import winreg

class RemoveIPsGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Remove IP Addresses")

        self.label = tk.Label(self.root, text="Enter IP addresses to remove (separated by commas):")
        self.label.pack(pady=10)

        self.ip_entry = tk.Entry(self.root, width=50)
        self.ip_entry.pack()

        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove_ips)
        self.remove_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

    def remove_ips(self):
        ips = self.ip_entry.get().split(",")
        for ip in ips:
            os.system(f'reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Terminal Server Client\LocalDevices\{ip.strip()}" /f')
        rdp_path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'Default.rdp')
        if os.path.isfile(rdp_path):
            os.system(f'attrib -h "{rdp_path}"')
            os.remove(rdp_path)
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Terminal Server Client\\Default", 0, winreg.KEY_ALL_ACCESS) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    value_name = winreg.EnumValue(key, i)[0]
                    if value_name.startswith('MRU'):
                        winreg.DeleteValue(key, value_name)
            self.status_label.config(text="IP addresses have been removed from the remote desktop client and Default.rdp has been deleted.")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RemoveIPsGUI()
    app.run()
