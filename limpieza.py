import miniupnpc
import socket
import threading

# Si el servidor fue importado desde otro proceso Python
try:
    from p2p_network import cerrar_servidor
except ImportError:
    cerrar_servidor = None

PUERTO_INICIAL = 5005
PUERTO_FINAL = 5037

# --- Cierre de puertos UPNP ---
upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

ip_local = upnp.lanaddr
cerrados = []
no_encontrados = []

for puerto in range(PUERTO_INICIAL, PUERTO_FINAL + 1):
    mapping = upnp.getspecificportmapping(puerto, 'TCP')
    if mapping:
        try:
            upnp.deleteportmapping(puerto, 'TCP')
            cerrados.append(puerto)
        except Exception as e:
            print(f"[!] Error al cerrar puerto {puerto}: {e}")
    else:
        no_encontrados.append(puerto)

print(f"[UPNP] Puertos cerrados correctamente: {cerrados}")
if no_encontrados:
    print(f"[UPNP] Puertos ya estaban cerrados: {no_encontrados}")

# --- Cierre de socket y hilo si está activo ---
if cerrar_servidor:
    try:
        cerrar_servidor()
        print("[Servidor] Socket y recursos cerrados correctamente.")
    except Exception as e:
        print(f"[Servidor] Error al cerrar servidor: {e}")
else:
    print("[Aviso] No se encontró función cerrar_servidor.")
