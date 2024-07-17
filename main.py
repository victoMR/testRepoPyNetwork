import tkinter as tk
from tkinter import messagebox
from scapy.all import ARP, Ether, srp
import netifaces as ni
import subprocess

# Función para obtener la dirección IP de la interfaz de red
def get_ip_address():
    interfaces = ni.interfaces()
    for interface in interfaces:
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            return addresses[ni.AF_INET][0]['addr']
    return None

# Función para escanear la red
def scan_network():
    ip = get_ip_address()
    if ip is None:
        messagebox.showerror("Error", "No se pudo obtener la dirección IP.")
        return []

    # Suponemos una máscara de subred /24
    ip_range = ip.rsplit('.', 1)[0] + '.1/24'
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# Función para bloquear un dispositivo (ejemplo simple usando iptables)
def block_device(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        messagebox.showinfo("Éxito", f"Dispositivo con IP {ip} bloqueado.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", f"No se pudo bloquear el dispositivo con IP {ip}.")

# Configuración de la interfaz gráfica
def create_gui():
    window = tk.Tk()
    window.title("Administrador de Red")

    frame = tk.Frame(window)
    frame.pack(pady=20)

    label = tk.Label(frame, text="Dispositivos conectados:")
    label.pack()

    listbox = tk.Listbox(frame, width=50)
    listbox.pack()

    def refresh_devices():
        listbox.delete(0, tk.END)
        devices = scan_network()
        if devices:
            for device in devices:
                listbox.insert(tk.END, f"IP: {device['ip']}, MAC: {device['mac']}")
        else:
            messagebox.showinfo("Información", "No se encontraron dispositivos.")

    def block_selected_device():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ningún dispositivo.")
            return

        device_info = listbox.get(selected[0])
        ip = device_info.split(',')[0].split(': ')[1]
        block_device(ip)

    refresh_button = tk.Button(frame, text="Refrescar", command=refresh_devices)
    refresh_button.pack(pady=5)

    block_button = tk.Button(frame, text="Bloquear", command=block_selected_device)
    block_button.pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
