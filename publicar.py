#!/usr/bin/env python3
"""Publica no Instagram da Manage Code o post agendado para a data de hoje.

Uso:
  IG_TOKEN=... python3 publicar.py              # publica o post de hoje (America/Sao_Paulo)
  IG_TOKEN=... python3 publicar.py --data 2026-12-01
  IG_TOKEN=... python3 publicar.py --teste      # só confere token, agenda e imagens; não publica
  IG_TOKEN=... python3 publicar.py --urls "url1,url2,..."   # posts do Canva: links exportados na hora
  python3 publicar.py --info                     # só mostra o que está agendado para hoje (sem token)
  IG_TOKEN=... python3 publicar.py --story posts/reel-portfolio-1/video.mp4   # publica um Story agora

Itens com "tipo": "reels" na agenda publicam posts/<post>/video.mp4 como Reel (com a legenda).
"""
import argparse, datetime, json, os, sys, time, urllib.parse, urllib.request, urllib.error

API_IG = "https://graph.instagram.com/v21.0"   # token IGAA (login do Instagram)
API_FB = "https://graph.facebook.com/v21.0"    # token EAA (login do Facebook / unificado)
API = API_IG
RAW_BASE = os.environ.get("RAW_BASE", "https://raw.githubusercontent.com/cheeenrique/managecode-instagram/main")
IG_USER_ID = os.environ.get("IG_USER_ID", "17841476644365202")  # @managecode
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


def esperar_pronto(container_id, tentativas=30):
    for _ in range(tentativas):
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
    ap.add_argument("--urls", help="links das imagens, separados por vírgula (posts do Canva)")
    ap.add_argument("--info", action="store_true", help="mostra o item de hoje em JSON e sai")
    ap.add_argument("--story", help="caminho no repo de uma imagem .jpg ou vídeo .mp4 para publicar como Story agora")
    a = ap.parse_args()

    hoje = a.data or (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).date().isoformat()
    agenda = json.load(open(os.path.join(AQUI, "agenda.json")))
    item = agenda.get(hoje)

    if a.info:
        print(json.dumps({"data": hoje, "item": item}, ensure_ascii=False))
        return

    global API
    if os.environ["IG_TOKEN"].startswith("EAA"):
        API = API_FB
        conta = chamar("GET", IG_USER_ID, fields="id,username")
        eu = {"user_id": conta["id"], "username": conta.get("username")}
    else:
        eu = chamar("GET", "me", fields="user_id,username")
    ig = eu["user_id"] if API == API_FB else "me"
    print(f"Conta: @{eu.get('username')} ({eu.get('user_id')}) via {API.split('/')[2]}")

    if a.story:
        url = f"{RAW_BASE}/{a.story}"
        if not url_ok(url):
            sys.exit(f"ERRO: arquivo inacessível: {url}")
        if a.teste:
            print(f"Teste OK: Story {a.story} acessível. Nada foi publicado."); return
        campo = "video_url" if a.story.endswith(".mp4") else "image_url"
        cont = chamar("POST", f"{ig}/media", media_type="STORIES", **{campo: url})
        esperar_pronto(cont["id"], 90)
        pub = chamar("POST", f"{ig}/media_publish", creation_id=cont["id"])
        print(f"STORY PUBLICADO: {a.story} (id {pub['id']})")
        return

    if not item:
        proximas = sorted(d for d in agenda if d > hoje)
        print(f"Nada agendado para {hoje}. Próximo: {proximas[0] if proximas else 'fila acabou'}")
        return

    post, n = item["post"], item.get("slides", 1)
    legenda = open(os.path.join(AQUI, "posts", post, "legenda.txt")).read().strip()
    reel = item.get("tipo") == "reels"
    if reel:
        urls = [f"{RAW_BASE}/posts/{post}/video.mp4"]
        if not url_ok(urls[0]):
            sys.exit("ERRO: vídeo inacessível: " + urls[0])
    elif a.urls:
        urls = [u.strip() for u in a.urls.split(",") if u.strip()]
        if len(urls) != n:
            sys.exit(f"ERRO: {post} tem {n} lâminas, mas vieram {len(urls)} links")
    elif item.get("canva_design_id"):
        sys.exit(f"ERRO: {post} está no Canva ({item['canva_design_id']}). Exporte em JPG e passe os links com --urls")
    else:
        urls = [f"{RAW_BASE}/posts/{post}/{i:02d}.jpg" for i in range(1, n + 1)]
        faltando = [u for u in urls if not url_ok(u)]
        if faltando:
            sys.exit("ERRO: imagens inacessíveis:\n" + "\n".join(faltando))
    print(f"{hoje}: {post} ({'reel' if reel else f'{n} lâmina(s)'})")

    # Evita publicar duas vezes o mesmo post
    recentes = chamar("GET", f"{ig}/media", fields="caption,permalink", limit=15).get("data", [])
    inicio = legenda[:80]
    for m in recentes:
        if (m.get("caption") or "").strip().startswith(inicio):
            print(f"Já publicado antes: {m.get('permalink')}. Nada a fazer.")
            return

    if a.teste:
        print("Teste OK: token válido, agenda e imagens acessíveis. Nada foi publicado.")
        return

    if reel:
        cont = chamar("POST", f"{ig}/media", media_type="REELS", video_url=urls[0],
                      caption=legenda, share_to_feed="true")
        esperar_pronto(cont["id"], 90)
    elif len(urls) == 1:
        cont = chamar("POST", f"{ig}/media", image_url=urls[0], caption=legenda)
    else:
        filhos = []
        for u in urls:
            c = chamar("POST", f"{ig}/media", image_url=u, is_carousel_item="true")
            filhos.append(c["id"])
        for f in filhos:
            esperar_pronto(f)
        cont = chamar("POST", f"{ig}/media", media_type="CAROUSEL",
                      children=",".join(filhos), caption=legenda)
    esperar_pronto(cont["id"])
    pub = chamar("POST", f"{ig}/media_publish", creation_id=cont["id"])
    link = chamar("GET", pub["id"], fields="permalink").get("permalink")
    print(f"PUBLICADO: {post} -> {link}")


if __name__ == "__main__":
    main()
