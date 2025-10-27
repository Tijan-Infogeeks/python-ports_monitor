import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psutil
import os
import signal

class PortMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moniteur de Ports - Temps Réel")
        self.root.geometry("1000x600")

        # Style ttkbootstrap
        style = tb.Style(theme="darkly")

        # --- Titre ---
        label = ttk.Label(root, text="Ports en écoute et occupés", font=("Segoe UI", 16, "bold"))
        label.pack(pady=10)

        # --- Barre de filtres ---
        filter_frame = ttk.Frame(root)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Filtrer par protocole :").grid(row=0, column=0, padx=5)
        self.proto_filter = ttk.Combobox(filter_frame, values=["", "TCP", "UDP"], width=8)
        self.proto_filter.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="PID :").grid(row=0, column=2, padx=5)
        self.pid_filter = ttk.Entry(filter_frame, width=10)
        self.pid_filter.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="Port :").grid(row=0, column=4, padx=5)
        self.port_filter = ttk.Entry(filter_frame, width=10)
        self.port_filter.grid(row=0, column=5, padx=5)

        filter_btn = ttk.Button(filter_frame, text="Appliquer le filtre", command=self.update_ports)
        filter_btn.grid(row=0, column=6, padx=10)

        clear_btn = ttk.Button(filter_frame, text="Réinitialiser", command=self.clear_filters)
        clear_btn.grid(row=0, column=7, padx=5)

        # --- Table ---
        columns = ("Proto", "Local Address", "Port", "PID", "Process Name", "State")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Barre de progression ---
        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill=X, padx=10, pady=(0, 10))

        # --- Boutons d’action ---
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=5)

        refresh_btn = ttk.Button(btn_frame, text="🔄 Rafraîchir maintenant", command=self.update_ports, bootstyle=INFO)
        refresh_btn.grid(row=0, column=0, padx=10)

        kill_btn = ttk.Button(btn_frame, text="💀 Tuer le processus sélectionné", command=self.kill_selected_process, bootstyle=DANGER)
        kill_btn.grid(row=0, column=1, padx=10)

        # --- Mise à jour initiale ---
        self.update_ports()

        # --- Fermeture propre ---
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_ports(self):
        """Retourne la liste des ports ouverts (TCP & UDP)"""
        ports = []
        try:
            result = subprocess.check_output("netstat -ano", shell=True, text=True, encoding="utf-8", errors="ignore")
            lines = result.strip().split("\n")
            for line in lines:
                if line.startswith("  "):  # lignes utiles
                    line = line.strip()
                    if line.startswith("TCP") or line.startswith("UDP"):
                        parts = line.split()
                        proto = parts[0]
                        local_address = parts[1]
                        pid = parts[-1]
                        state = parts[3] if proto == "TCP" and len(parts) >= 4 else "LISTENING"

                        # Extraction du port
                        if ":" in local_address:
                            port = local_address.split(":")[-1]
                        else:
                            port = "?"

                        # Nom du processus
                        try:
                            process = psutil.Process(int(pid))
                            name = process.name()
                        except Exception:
                            name = "Inconnu"

                        ports.append((proto, local_address, port, pid, name, state))
        except Exception as e:
            print("Erreur récupération des ports:", e)
        return ports

    def update_ports(self):
        """Met à jour la table avec filtres"""
        self.progress.start()
        self.tree.delete(*self.tree.get_children())
        ports = self.get_ports()

        # Application des filtres
        proto_f = self.proto_filter.get().strip().upper()
        pid_f = self.pid_filter.get().strip()
        port_f = self.port_filter.get().strip()

        for port in ports:
            proto, addr, p, pid, name, state = port

            if proto_f and proto != proto_f:
                continue
            if pid_f and pid_f != pid:
                continue
            if port_f and port_f != p:
                continue

            self.tree.insert("", "end", values=port)

        self.progress.stop()

    def clear_filters(self):
        """Réinitialise les filtres"""
        self.proto_filter.set("")
        self.pid_filter.delete(0, tk.END)
        self.port_filter.delete(0, tk.END)
        self.update_ports()

    def kill_selected_process(self):
        """Tue le processus du port sélectionné"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aucun élément", "Veuillez sélectionner un processus à tuer.")
            return

        values = self.tree.item(selected[0], "values")
        pid = values[3]
        name = values[4]

        try:
            process = psutil.Process(int(pid))
            process.kill()
            messagebox.showinfo("Succès", f"Le processus '{name}' (PID {pid}) a été tué avec succès.")
            self.update_ports()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de tuer le processus {pid}.\n\n{e}")

    def on_close(self):
        """Ferme proprement"""
        self.root.destroy()


if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = PortMonitorApp(root)
    root.mainloop()
