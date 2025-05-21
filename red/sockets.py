import socket
import threading
import time

_servidor_socket = None
_servidor_puerto = None
_servidor_hilo = None
_cerrar_evento = threading.Event()

def iniciar_servidor(puerto, on_conexion):
    """Inicia un servidor que acepta una conexión entrante."""
    def servidor():
        global _servidor_socket
        try:
            _servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            _servidor_socket.bind(("", puerto))
            _servidor_socket.listen(1)
            _servidor_socket.settimeout(1.0)
            print(f"[Servidor] Escuchando en puerto {puerto}...")

            while not _cerrar_evento.is_set():
                try:
                    cliente_socket, direccion = _servidor_socket.accept()
                    print(f"[Servidor] Conectado con: {direccion}")
                    on_conexion(cliente_socket, direccion)
                    break
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"[Servidor] Error: {e}")
        finally:
            if _servidor_socket:
                try:
                    _servidor_socket.close()
                    print("[Servidor] Socket cerrado.")
                except Exception as e:
                    print(f"[Servidor] Error al cerrar socket: {e}")

    global _servidor_puerto, _servidor_hilo
    _cerrar_evento.clear()
    _servidor_puerto = puerto
    _servidor_hilo = threading.Thread(target=servidor, daemon=True)
    _servidor_hilo.start()

def conectar_con_servidor(ip, puerto, on_conexion):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, puerto))
        print(f"[Cliente] Conectado a {ip}:{puerto}")
        on_conexion(cliente_socket, (ip, puerto))
    except Exception as e:
        print(f"[Cliente] Error de conexión: {e}")

def enviar_mensaje(sock, mensaje):
    try:
        sock.sendall(mensaje.encode('utf-8'))
        print(f"[Socket] Enviado: {mensaje}")
    except Exception as e:
        print(f"[Socket] Error al enviar: {e}")

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

def cerrar_servidor():
    global _servidor_socket, _servidor_puerto, _servidor_hilo
    _cerrar_evento.set()

    if _servidor_puerto:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dummy:
                dummy.connect(("127.0.0.1", _servidor_puerto))
                print(f"[Dummy] Conexión falsa enviada a {_servidor_puerto}")
        except Exception as e:
            print(f"[Dummy] Error: {e}")

    if _servidor_hilo:
        _servidor_hilo.join(timeout=3.0)
        time.sleep(0.5)
        print("[Servidor] Hilo finalizado.")
        _servidor_hilo = None