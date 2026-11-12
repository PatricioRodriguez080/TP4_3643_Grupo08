
import csv
import getpass
import requests

BASE = "http://localhost:58000/api/v1"

clave = getpass.getpass("Clave del NC: ")

r = requests.post(f"{BASE}/ticket", json={"username": "cisco", "password": clave})
r.raise_for_status()
ticket = r.json()["response"]["serviceTicket"]
headers = {"X-Auth-Token": ticket}

equipos = requests.get(f"{BASE}/network-device", headers=headers).json()["response"]
hosts = requests.get(f"{BASE}/host", headers=headers).json()["response"]

with open("inventario.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tipo", "nombre", "ip", "plataforma_o_mac", "conectado_a"])

    for e in equipos:
        w.writerow([
            "equipo",
            e.get("hostname") or "SIN_HOSTNAME",
            e.get("managementIpAddress") or "",
            e.get("platformId") or "",
            "",
        ])

    for h in hosts:
        conectado = f'{h.get("connectedNetworkDeviceName") or ""} {h.get("connectedInterfaceName") or ""}'.strip()
        w.writerow([
            "host",
            h.get("hostName") or "SIN_HOSTNAME",
            h.get("hostIp") or "",
            h.get("hostMac") or "",
            conectado,
        ])

print(f"{len(equipos)} equipos y {len(hosts)} hosts en inventario.csv")
