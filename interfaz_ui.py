import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from red.upnp import limpiar_puertos_abiertos

class ChatApp:
    def __init__(self, master, gestor_conexion):
        self.master = master
        self.conexion = gestor_conexion
        master.title("Chat P2P")
        master.geometry("1020x800")
        master.configure(bg="black")

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.estado_actual = None

        self.main_menu = tk.Frame(master, bg="black")
        self.host_button = tk.Button(self.main_menu, text="Hostear", command=self.mostrar_menu_host,
                                      bg="gray20", fg="white", font=("Arial", 18), width=20, height=2)
        self.join_button = tk.Button(self.main_menu, text="Unirse", command=self.mostrar_menu_join,
                                      bg="gray20", fg="white", font=("Arial", 18), width=20, height=2)
        self.limpieza_button = tk.Button(self.main_menu, text="Forzar limpieza", command=self.forzar_limpieza,
                                         bg="darkred", fg="white", font=("Arial", 14), width=20, height=2)

        self.host_button.pack(pady=30)
        self.join_button.pack(pady=10)
        self.limpieza_button.pack(pady=10)
        self.main_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.menu_host = tk.Frame(master, bg="black")
        self.info_label_host = tk.Label(self.menu_host, text="", bg="black", fg="white", font=("Arial", 16))
        self.boton_volver1 = tk.Button(self.menu_host, text="Volver", command=self.volver_de_host,
                                       bg="gray30", fg="white", font=("Arial", 14))
        self.boton_pruebas = tk.Button(
            self.menu_host, text="PRUEBAS", command=self.chat_prueba, bg="darkorange",
            fg="black", font=("Arial", 14))
        self.info_label_host.pack(pady=20)
        self.boton_volver1.pack(pady=10)
        self.boton_pruebas.pack(pady=10)

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
        resultado = limpiar_puertos_abiertos()
        if resultado['abiertos']:
            messagebox.showwarning("Puertos abiertos", "No se puede cerrar la app. Ejecute 'Forzar limpieza' para cerrar puertos abiertos.")
            return
        self.conexion.cerrar_todo()
        self.master.destroy()

    def forzar_limpieza(self):
        resultado = limpiar_puertos_abiertos()
        if resultado['abiertos']:
            messagebox.showinfo("Limpieza parcial", f"Se cerraron algunos puertos.",
                                detail=f"Puertos no cerrados: {resultado['abiertos']}")
        else:
            messagebox.showinfo("Limpieza exitosa", "Todos los puertos han sido cerrados correctamente.")

    def ocultar_todos_los_menus(self):
        self.main_menu.place_forget()
        self.menu_host.place_forget()
        self.menu_join.place_forget()

    def mostrar_menu_principal(self):
        self.ocultar_todos_los_menus()
        self.main_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def volver_de_host(self):
        self.conexion.cerrar()
        self.mostrar_menu_principal()

    def mostrar_menu_host(self):
        self.ocultar_todos_los_menus()
        self.menu_host.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.host_chat()

    def mostrar_menu_join(self):
        self.ocultar_todos_los_menus()
        self.menu_join.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def host_chat(self):
        resultado = self.conexion.hostear()
        if resultado['exito']:
            self.info_label_host.config(text=f"Host listo\nComparte este código:\n{resultado['codigo']}")
        else:
            self.info_label_host.config(text=f"Error:\n{resultado['error']}")

    def join_chat(self):
        code = self.join_entry.get()
        if code:
            try:
                ip, puerto = code.split(":")
                puerto = int(puerto)
                self.conexion.unirse(ip, puerto, lambda sock: self.chat_prueba(sock))
            except Exception as e:
                self.info_label_join.config(text=f"Error:\n{e}")

    def chat_prueba(self, socket=None):
        from Chat_Window import abrir_chat_de_prueba
        abrir_chat_de_prueba(self.master, socket)
