import miniupnpc

PUERTO_INICIAL = 5005
PUERTO_MAXIMO = 5030

def abrir_puerto_upnp(puerto_deseado=PUERTO_INICIAL):
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        upnp.discover()
        upnp.selectigd()
        ip_local = upnp.lanaddr

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

def cerrar_puerto_upnp(puerto):
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        upnp.discover()
        upnp.selectigd()

        eliminado = upnp.deleteportmapping(puerto, 'TCP')
        if eliminado:
            print(f"[UPNP] Puerto {puerto} eliminado correctamente.")
        else:
            print(f"[UPNP] Falló el borrado del puerto {puerto}.")
        return eliminado
    except Exception as e:
        print(f"[UPNP] Error al intentar liberar el puerto: {e}")
        return False

def limpiar_puertos_abiertos():
    try:
        upnp_client = miniupnpc.UPnP()
        upnp_client.discoverdelay = 200
        upnp_client.discover()
        upnp_client.selectigd()

        cerrados = []
        abiertos = []

        for puerto in range(PUERTO_INICIAL, PUERTO_MAXIMO + 1):
            mapping = upnp_client.getspecificportmapping(puerto, 'TCP')
            if mapping:
                try:
                    upnp_client.deleteportmapping(puerto, 'TCP')
                    cerrados.append(puerto)
                except Exception as e:
                    print(f"[UPNP] Error al cerrar puerto {puerto}: {e}")
                    abiertos.append(puerto)
        return {
            'cerrados': cerrados,
            'abiertos': abiertos
        }
    except Exception as e:
        print(f"[UPNP] Error general en limpieza: {e}")
        return {
            'cerrados': [],
            'abiertos': list(range(PUERTO_INICIAL, PUERTO_MAXIMO + 1))
        }
