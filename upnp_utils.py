import miniupnpc
import socket

PUERTO_INICIAL = 5005
PUERTO_MAXIMO = 5030


def abrir_puerto_upnp(puerto_deseado=PUERTO_INICIAL):
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        upnp.discover()  # Descubre dispositivos UPNP
        upnp.selectigd()  # Selecciona el gateway IGD (router)

        ip_local = upnp.lanaddr

        # Validar que el puerto deseado esté dentro del rango
        if puerto_deseado < PUERTO_INICIAL or puerto_deseado > PUERTO_MAXIMO:
            puerto_deseado = PUERTO_INICIAL

        puerto = puerto_deseado
        print(f"[UPNP] Intentando abrir puerto {puerto}...")
        while puerto <= PUERTO_MAXIMO:
            if upnp.getspecificportmapping(puerto, 'TCP') is None:
                try:
                    upnp.addportmapping(puerto, 'TCP', ip_local, puerto, 'Chat P2P', '')
                    print(f"[UPNP] Puerto {puerto} ABIERTO correctamente.")
                    return {
                        'ip_local': ip_local,
                        'puerto': puerto,
                        'exito': True
                    }
                except Exception as e:
                    print(f"[UPNP] Falló abrir puerto {puerto}: {e}")
            else:
                print(f"[UPNP] Puerto {puerto} ya está ocupado.")
            puerto += 1

        return {
            'error': f"No se pudo abrir ningún puerto entre {PUERTO_INICIAL} y {PUERTO_MAXIMO}.",
            'exito': False
        }

    except Exception as e:
        return {
            'error': str(e),
            'exito': False
        }


if __name__ == "__main__":
    resultado = abrir_puerto_upnp()
    if resultado["exito"]:
        print(f"Puerto abierto: {resultado['ip_local']}:{resultado['puerto']}")
    else:
        print(f"Error: {resultado}")
