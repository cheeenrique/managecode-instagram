#!/usr/bin/env python3
"""Publica no Instagram da Manage Code o post agendado para a data de hoje.

Uso:
  IG_TOKEN=... python3 publicar.py              # publica o post de hoje (America/Sao_Paulo)
  IG_TOKEN=... python3 publicar.py --data 2026-12-01
  IG_TOKEN=... python3 publicar.py --teste      # só confere token, agenda e imagens; não publica
"""
import argparse, datetime, json, os, sys, time, urllib.parse, urllib.request, urllib.error

API = "https://graph.instagram.com/v21.0"
RAW_BASE = os.environ.get("RAW_BASE", "https://raw.githubusercontent.com/cheeenrique/managecode-instagram/main")
AQUI = os.path.dirname(os.path.abspath(__file__))


def chamar(metodo, caminho, **params):
    params["access_token"] = os.environ["IG_TOKEN"]
    dados = urllib.parse.urlencode(params).encode()
    url = f"{API}/{caminho}"
    if metodo == "GET":
        req = urllib.request.Request(f"{url}?{dados.decode()}")
    else:
        req = urllib.request.Request(url, data=dados, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        sys.exit(f"ERRO da API ({e.code}) em {caminho}: {corpo}")


def esperar_pronto(container_id):
    for _ in range(30):
        st = chamar("GET", container_id, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"ERRO: container {container_id} ficou {st}")
        time.sleep(5)
    sys.exit(f"ERRO: container {container_id} não ficou pronto a tempo")


def url_ok(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()

    hoje = a.data or (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()
    agenda = json.load(open(os.path.join(AQUI, "agenda.json")))
    item = agenda.get(hoje)

    eu = chamar("GET", "me", fields="user_id,username")
    print(f"Conta: @{eu.get('username')} ({eu.get('user_id')})")

    if not item:
        proximas = sorted(d for d in agenda if d > hoje)
        print(f"Nada agendado para {hoje}. Próximo: {proximas[0] if proximas else 'fila acabou'}")
        return

    post, n = item["post"], item["slides"]
    legenda = open(os.path.join(AQUI, "posts", post, "legenda.txt")).read().strip()
    urls = [f"{RAW_BASE}/posts/{post}/{i:02d}.jpg" for i in range(1, n + 1)]
    print(f"{hoje}: {post} ({n} lâminas)")

    faltando = [u for u in urls if not url_ok(u)]
    if faltando:
        sys.exit("ERRO: imagens inacessíveis:\n" + "\n".join(faltando))

    # Evita publicar duas vezes o mesmo post
    recentes = chamar("GET", "me/media", fields="caption,permalink", limit=15).get("data", [])
    inicio = legenda[:80]
    for m in recentes:
        if (m.get("caption") or "").strip().startswith(inicio):
            print(f"Já publicado antes: {m.get('permalink')}. Nada a fazer.")
            return

    if a.teste:
        print("Teste OK: token válido, agenda e imagens acessíveis. Nada foi publicado.")
        return

    filhos = []
    for u in urls:
        c = chamar("POST", "me/media", image_url=u, is_carousel_item="true")
        filhos.append(c["id"])
    for f in filhos:
        esperar_pronto(f)

    carrossel = chamar("POST", "me/media", media_type="CAROUSEL",
                       children=",".join(filhos), caption=legenda)
    esperar_pronto(carrossel["id"])
    pub = chamar("POST", "me/media_publish", creation_id=carrossel["id"])
    link = chamar("GET", pub["id"], fields="permalink").get("permalink")
    print(f"PUBLICADO: {post} -> {link}")


if __name__ == "__main__":
    main()
