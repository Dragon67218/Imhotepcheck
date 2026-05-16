#!/usr/bin/env python3
# ==========================================
#     📡 Check M3U Pro v2 - Hacker Edition
#     Desarrollador: IMHOTEP
# ==========================================

import urllib.request
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# 🎨 COLORES
R = "\033[91m"
B = "\033[94m"
W = "\033[97m"
X = "\033[0m"

INPUT_FILE = "lista.m3u"
OUTPUT_FILE = "lista_limpia.m3u"

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 🔊 SONIDO
def beep():
    print("\a")

# 🧠 BANNER
def banner():
    print(B + "==========================================" + X)
    print(W + "     📡 Check M3U Pro v2 - Hacker Edition" + X)
    print(B + "------------------------------------------" + X)
    print(R + "        👨‍💻 IMHOTEP" + X)
    print(B + "==========================================" + X)

# 🎮 MENÚ
def menu():
    print(W + "\n[1] Iniciar escaneo")
    print("[2] Ver info")
    print("[3] Salir\n" + X)
    return input(R + "Selecciona opción > " + X)

# 📊 PROGRESO
def progress(done, total):
    percent = int((done/total)*100)
    bar = "█" * (percent//5) + "-" * (20 - percent//5)
    sys.stdout.write(f"\r{B}[{bar}] {percent}%{X}")
    sys.stdout.flush()

# 🔎 CHECK STREAM
def check(url):
    try:
        start = time.time()
        req = urllib.request.Request(url, headers=HEADERS)
        res = urllib.request.urlopen(req, timeout=8)

        ctype = res.info().get('Content-Type', '')
        latency = round(time.time() - start, 2)

        if 'video' in ctype or 'mpegurl' in ctype:
            return (url, True, latency)
    except:
        pass
    return (url, False, None)

# 📂 CARGAR M3U
def load():
    urls = []
    with open(INPUT_FILE, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("http"):
                urls.append(line.strip())
    return urls

# 💾 GUARDAR
def save(urls):
    with open(OUTPUT_FILE, "w") as f:
        for u in urls:
            f.write(u + "\n")

# 🚀 ESCANEO
def scan():
    urls = load()
    total = len(urls)

    print(B + f"\n🔎 Escaneando {total} streams...\n" + X)

    results = []
    done = 0

    def worker(url):
        nonlocal done
        r = check(url)
        done += 1
        progress(done, total)
        return r

    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(worker, urls))

    print("\n")

    working = [r[0] for r in results if r[1]]

    print(B + "==========================================" + X)
    print(W + f"✅ Activos: {len(working)}/{total}" + X)
    print(B + "==========================================" + X)

    save(working)

    if working:
        print(R + "\n🚨 SCAN COMPLETADO 🚨" + X)
        beep(); beep()
    else:
        print(R + "\n⚠️ NO HAY STREAMS ACTIVOS ⚠️" + X)
        beep()

# ℹ INFO
def info():
    print(W + """
Check M3U Pro v2
Herramienta avanzada de verificación IPTV

Funciones:
- Escaneo rápido
- Filtrado inteligente
- Exportación limpia
- UI estilo hacker

Desarrollador: IMHOTEP
""" + X)

# 🎯 MAIN
def main():
    banner()
    while True:
        op = menu()

        if op == "1":
            scan()
        elif op == "2":
            info()
        elif op == "3":
            print(R + "\nSaliendo...\n" + X)
            break
        else:
            print("Opción inválida")

# -----------------------------
if __name__ == "__main__":
    main()