import tkinter as tk
import threading
from p2p_network import enviar_mensaje as enviar_socket, escuchar_mensajes, cerrar_servidor

def abrir_chat_de_prueba(master, socket=None):
    ventana_chat = tk.Toplevel(master)
    ventana_chat.title("Chat P2P")
    ventana_chat.geometry("600x500")
    ventana_chat.configure(bg="black")

    texto_chat = tk.Text(ventana_chat, state='disabled', bg="black", fg="white", font=("Arial", 12))
    texto_chat.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    canvas_mensaje = tk.Frame(ventana_chat, bg="black")
    canvas_mensaje.pack(fill=tk.X, padx=10, pady=5)

    entry_mensaje = tk.Entry(canvas_mensaje, font=("Arial", 12))
    entry_mensaje.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

    def agregar_mensaje(mensaje):
        texto_chat.configure(state='normal')
        texto_chat.insert(tk.END, mensaje + "\n")
        texto_chat.configure(state='disabled')
        texto_chat.see(tk.END)

    def enviar():
        mensaje = entry_mensaje.get()
        if mensaje and socket:
            try:
                enviar_socket(socket, mensaje)
                agregar_mensaje(f"Tú: {mensaje}")
                entry_mensaje.delete(0, tk.END)
            except Exception as e:
                agregar_mensaje(f"[Error al enviar]: {e}")

    boton_enviar = tk.Button(canvas_mensaje, text="Enviar", command=enviar, font=("Arial", 12))
    boton_enviar.pack(side=tk.RIGHT)

    boton_cerrar = tk.Button(ventana_chat, text="Cerrar Conexión", font=("Arial", 10), bg="red", fg="white", command=lambda: cerrar_chat())
    boton_cerrar.pack(pady=5)

    def cerrar_chat():
        agregar_mensaje("[Sistema] Cerrando conexión...")
        try:
            if socket:
                socket.close()
                agregar_mensaje("[Sistema] Socket cerrado correctamente.")
        except Exception as e:
            agregar_mensaje(f"[Error al cerrar socket]: {e}")
        cerrar_servidor()
        ventana_chat.destroy()

    # Captura de cierre por la cruz (WM_DELETE_WINDOW)
    ventana_chat.protocol("WM_DELETE_WINDOW", cerrar_chat)

    if socket:
        def recibir():
            def callback(mensaje):
                ventana_chat.after(0, agregar_mensaje, f"Amigo: {mensaje}")
            escuchar_mensajes(socket, callback)

        threading.Thread(target=recibir, daemon=True).start()
    else:
        agregar_mensaje("[Sistema]: Sin conexión activa. Modo prueba.")
