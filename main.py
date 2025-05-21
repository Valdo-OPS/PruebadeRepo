import tkinter as tk
import os
import sys
import subprocess
import time

from interfaz_ui import ChatApp
from red.gestor import GestorConexion

os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Si se lanza desde limpieza, no continuar
if os.environ.get("LIMPIEZA_MODE") == "1":
    print("[Main] Cancelando ejecución porque fue lanzado desde limpieza.")
    sys.exit(0)

def ejecutar_limpieza():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    ruta_script = os.path.join(base_dir, "limpieza.py")
    print(f"[Limpieza] Ejecutando limpieza.py desde: {ruta_script}")

    try:
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            [sys.executable, ruta_script],
            env={**os.environ, "LIMPIEZA_MODE": "1"},
            creationflags=DETACHED_PROCESS
        )
        print("[Limpieza] limpieza.py lanzado como subproceso.")
        time.sleep(0.8)
    except Exception as e:
        print(f"[Limpieza] Error al ejecutar limpieza.py: {e}")

if __name__ == "__main__":
    try:
        print("[Sistema] Iniciando interfaz ChatApp")
        root = tk.Tk()
        gestor = GestorConexion()
        app = ChatApp(root, gestor)

        def on_close():
            print("[Sistema] Cierre solicitado por usuario")
            gestor.cerrar_todo()
            ejecutar_limpieza()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()
    except Exception as e:
        print(f"[ERROR] Excepción fatal: {e}")
