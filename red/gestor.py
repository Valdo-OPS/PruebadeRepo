import threading
from red import sockets, upnp

class GestorConexion:
    def __init__(self):
        self.socket = None
        self.thread = None
        self.puerto = None
        self.chat_callback = None

    def hostear(self):
        resultado = upnp.abrir_puerto_upnp()
        if not resultado['exito']:
            return resultado

        self.puerto = resultado['puerto']

        def on_conexion(sock, direccion):
            if direccion[0] == '127.0.0.1':
                print("[Gestor] Conexión dummy ignorada")
                sock.close()
                return
            self.socket = sock
            if self.chat_callback:
                self.chat_callback(sock)

        sockets.iniciar_servidor(self.puerto, on_conexion)

        return {
            'codigo': f"{resultado['ip_local']}:{self.puerto}",
            'exito': True
        }

    def unirse(self, ip, puerto, on_conectado):
        def al_conectar(sock, direccion):
            self.socket = sock
            if on_conectado:
                on_conectado(sock)
        sockets.conectar_con_servidor(ip, puerto, al_conectar)

    def enviar(self, mensaje):
        if self.socket:
            sockets.enviar_mensaje(self.socket, mensaje)

    def escuchar(self, callback):
        if self.socket:
            sockets.escuchar_mensajes(self.socket, callback)

    def cerrar(self):
        sockets.cerrar_servidor()
        if self.socket:
            try:
                self.socket.close()
                print("[Gestor] Socket cerrado")
            except Exception as e:
                print(f"[Gestor] Error al cerrar socket: {e}")
            self.socket = None

    def cerrar_todo(self):
        self.cerrar()
        try:
            from limpieza.limpieza import cerrar_servidor as cerrar_secundario
            if cerrar_secundario:
                cerrar_secundario()
        except Exception as e:
            print(f"[Gestor] Error en limpieza secundaria: {e}")
