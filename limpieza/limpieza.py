import miniupnpc
from red import upnp
from red import sockets

PUERTO_INICIAL = 5005
PUERTO_FINAL = 5037

# --- Cierre de puertos UPNP ---
def limpiar_puertos():
    upnp_client = miniupnpc.UPnP()
    upnp_client.discoverdelay = 200
    upnp_client.discover()
    upnp_client.selectigd()

    cerrados = []
    no_encontrados = []

    for puerto in range(PUERTO_INICIAL, PUERTO_FINAL + 1):
        mapping = upnp_client.getspecificportmapping(puerto, 'TCP')
        if mapping:
            try:
                upnp_client.deleteportmapping(puerto, 'TCP')
                cerrados.append(puerto)
            except Exception as e:
                print(f"[Limpieza] Error al cerrar puerto {puerto}: {e}")
        else:
            no_encontrados.append(puerto)

    print(f"[Limpieza] Puertos cerrados: {cerrados}")
    if no_encontrados:
        print(f"[Limpieza] Ya cerrados o no existentes: {no_encontrados}")

# --- Cierre de socket y servidor si están activos ---
def cerrar_servidor():
    try:
        sockets.cerrar_servidor()
        print("[Limpieza] Servidor cerrado correctamente.")
    except Exception as e:
        print(f"[Limpieza] Error al cerrar servidor: {e}")

if __name__ == "__main__":
    print("[Limpieza] Iniciando limpieza...")
    limpiar_puertos()
    cerrar_servidor()
    print("[Limpieza] Finalizado.")
