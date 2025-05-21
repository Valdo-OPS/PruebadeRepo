import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
import os
import subprocess
import sys

# --- Míos ---
from upnp_utils import abrir_puerto_upnp
from p2p_network import iniciar_servidor, cerrar_servidor, conectar_con_servidor
from Chat_Window import abrir_chat_de_prueba

os.environ['TK_SILENCE_DEPRECATION'] = '1'

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat P2P")
        master.geometry("1020x800")
        master.configure(bg="black")

        # Capturar cierre de ventana
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Estados
        self.estado_actual = None

        # Menú principal
        self.main_menu = tk.Frame(master, bg="black")
        self.host_button = tk.Button(self.main_menu, text="Hostear", command=self.mostrar_menu_host,
                                      bg="gray20", fg="white", font=("Arial", 18), width=20, height=2)
        self.join_button = tk.Button(self.main_menu, text="Unirse", command=self.mostrar_menu_join,
                                      bg="gray20", fg="white", font=("Arial", 18), width=20, height=2)
        self.host_button.pack(pady=30)
        self.join_button.pack(pady=30)
        self.main_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Menú host
        self.menu_host = tk.Frame(master, bg="black")
        self.info_label_host = tk.Label(self.menu_host, text="", bg="black", fg="white", font=("Arial", 16))
        self.boton_volver1 = tk.Button(self.menu_host, text="Volver", command=self.volver_de_host,
                                       bg="gray30", fg="white", font=("Arial", 14))
        self.boton_pruebas = tk.Button(
            self.menu_host,
            text="PRUEBAS",
            command=lambda: abrir_chat_de_prueba(self.master),
            bg="darkorange",
            fg="black",
            font=("Arial", 14)
        )
        self.info_label_host.pack(pady=20)
        self.boton_volver1.pack(pady=10)
        self.boton_pruebas.pack(pady=10)

        # Menú join
        self.menu_join = tk.Frame(master, bg="black")
        self.info_label_join = tk.Label(self.menu_join, text="Ingresa el código del host (IP:PUERTO):",
                                        bg="black", fg="white", font=("Arial", 16))
        self.join_entry = tk.Entry(self.menu_join, font=("Arial", 16), width=30)
        self.join_submit = tk.Button(self.menu_join, text="Conectar", command=self.join_chat,
                                     bg="gray30", fg="white", font=("Arial", 14))
        self.boton_volver2 = tk.Button(self.menu_join, text="Volver", command=self.mostrar_menu_principal,
                                       bg="gray30", fg="white", font=("Arial", 14))
        self.info_label_join.pack(pady=10)
        self.join_entry.pack(pady=5)
        self.join_submit.pack(pady=5)
        self.boton_volver2.pack(pady=10)

    def on_close(self):
        print("[Sistema] Cerrando aplicación...")
        cerrar_servidor()

        # Ejecutar limpieza.py como subprocess externo
        ruta_script = os.path.join(os.getcwd(), "limpieza.py")
        try:
            subprocess.run([sys.executable, ruta_script], check=True)
            print("[Limpieza] limpieza.py ejecutado con éxito.")
        except Exception as e:
            print(f"[Limpieza] Error al ejecutar limpieza.py: {e}")

        self.master.destroy()

    def ocultar_todos_los_menus(self):
        self.main_menu.place_forget()
        self.menu_host.place_forget()
        self.menu_join.place_forget()

    def mostrar_menu_principal(self):
        self.ocultar_todos_los_menus()
        self.main_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def volver_de_host(self):
        print("[Volver] Cierre forzado del servidor")  #Mensaje de control
        cerrar_servidor()  # Este ya hace todo: socket + hilo + puerto
        self.mostrar_menu_principal()

    def mostrar_menu_host(self):
        self.ocultar_todos_los_menus()
        self.menu_host.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.host_chat()

    def mostrar_menu_join(self):
        self.ocultar_todos_los_menus()
        self.menu_join.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def host_chat(self):
        print(">>> Ejecutando host_chat")  # DEBUG

        resultado = abrir_puerto_upnp()
        if resultado['exito']:
            ip = resultado['ip_local']
            puerto = resultado['puerto']
            codigo = f"{ip}:{puerto}"
            self.info_label_host.config(text=f"Host listo\nComparte este código con tu amigo:\n{codigo}")

            def on_conexion(cliente, direccion):
                if direccion[0] == '127.0.0.1':
                    print("[Servidor] Conexión dummy ignorada.")
                    cliente.close()
                    return  # No abrir chat

                self.info_label_host.config(text=f"Conexión recibida de {direccion[0]}:{direccion[1]}")
                cliente.close()
                self.abrir_chat_de_prueba()

        else:
            self.info_label_host.config(text=f"Error al abrir puerto:\n{resultado['error']}")

    def join_chat(self):
        print(">>> Ejecutando join_chat")  # DEBUG

        code = self.join_entry.get()
        if code:
            try:
                ip, puerto = code.split(":")
                puerto = int(puerto)

                def on_conexion(cliente_socket, direccion):
                    self.info_label_join.config(text=f"Conectado con éxito a {ip}:{puerto}")
                    abrir_chat_de_prueba(self.master, cliente_socket)

                conectar_con_servidor(ip, puerto, on_conexion)

            except Exception as e:
                self.info_label_join.config(text=f"Error al conectar:\n{e}")


if __name__ == "__main__":
    try:
        print("Interfaz ChatApp iniciada")
        root = tk.Tk()
        app = ChatApp(root)
        root.mainloop()
    except Exception as e:
        print(f"ERROR: {e}")
