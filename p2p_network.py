import socket
import threading
import miniupnpc
import time

servidor_socket = None
servidor_puerto = None
cliente_socket = None
servidor_hilo = None
cerrar_evento = threading.Event()

# -----------------------------
# Servidor
# -----------------------------
def iniciar_servidor(puerto, on_conexion):
    """Inicia un servidor que acepta una conexión entrante."""
    def servidor():
        global servidor_socket, cliente_socket
        try:
            servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor_socket.bind(("", puerto))
            servidor_socket.listen(1)
            servidor_socket.settimeout(1.0)  # timeout de 1 segundo
            print(f"[Servidor] Escuchando en puerto {puerto}...")

            while not cerrar_evento.is_set():
                try:
                    cliente_socket, direccion = servidor_socket.accept()
                    print(f"[Servidor] Conectado con: {direccion}")
                    on_conexion(cliente_socket, direccion)
                    break
                except socket.timeout:
                    continue

        except OSError as e:
            print(f"[Servidor] accept() interrumpido: {e}")
        except Exception as e:
            print(f"[Servidor] Error general: {e}")
        finally:
            if servidor_socket:
                try:
                    servidor_socket.close()
                    print("[Servidor] Socket cerrado.")
                except Exception as e:
                    print(f"[Servidor] Error al cerrar: {e}")
            servidor_socket = None
            print("[Servidor] Hilo del servidor finalizado.")

    global servidor_puerto, servidor_hilo
    cerrar_evento.clear()
    servidor_puerto = puerto
    servidor_hilo = threading.Thread(target=servidor, daemon=True)
    servidor_hilo.start()

# -----------------------------
# Cliente
# -----------------------------
def conectar_con_servidor(ip, puerto, on_conexion):
    """Conecta como cliente a un host."""
    global cliente_socket
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, puerto))
        print(f"[Cliente] Conectado a {ip}:{puerto}")
        on_conexion(cliente_socket, (ip, puerto))
    except Exception as e:
        print(f"[Cliente] Error de conexión: {e}")

# -----------------------------
# Enviar mensaje
# -----------------------------
def enviar_mensaje(sock, mensaje):
    try:
        sock.sendall(mensaje.encode('utf-8'))
        print(f"[Socket] Enviado: {mensaje}")
    except Exception as e:
        print(f"[Socket] Error al enviar: {e}")

# -----------------------------
# Escuchar mensajes entrantes
# -----------------------------
def escuchar_mensajes(sock, callback):
    def recibir():
        while True:
            try:
                datos = sock.recv(1024)
                if not datos:
                    break
                mensaje = datos.decode('utf-8')
                callback(mensaje)
            except Exception as e:
                print(f"[Socket] Error al recibir: {e}")
                break
    hilo = threading.Thread(target=recibir, daemon=True)
    hilo.start()

# -----------------------------
# Cerrar servidor manualmente
# -----------------------------
def cerrar_servidor():
    global servidor_socket, servidor_puerto, servidor_hilo
    cerrar_evento.set()

    # 1. Desbloquea accept()
    if servidor_puerto:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dummy:
                dummy.connect(("127.0.0.1", servidor_puerto))
                print(f"[Dummy] Conexión enviada a {servidor_puerto} para desbloquear accept().")
        except Exception as e:
            print(f"[Dummy] Falló: {e}")

    # 2. Espera a que el hilo termine correctamente
    if servidor_hilo:
        servidor_hilo.join(timeout=3.0)
        time.sleep(0.5)
        print("[Servidor] Hilo finalizado tras join.")
        servidor_hilo = None

    # 3. Elimina el mapeo del puerto en el router
    if servidor_puerto:
        try:
            upnp = miniupnpc.UPnP()
            upnp.discover()
            upnp.selectigd()

            eliminado = upnp.deleteportmapping(servidor_puerto, 'TCP')
            if eliminado:
                print(f"[UPNP] Puerto {servidor_puerto} eliminado del router.")
            else:
                print(f"[UPNP] Falló el borrado del puerto {servidor_puerto} (no existía o no fue aceptado).")
        except Exception as e:
            print(f"[UPNP] Error al intentar liberar el puerto: {e}")
        servidor_puerto = None
