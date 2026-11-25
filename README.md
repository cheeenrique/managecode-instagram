# Manage Code · Instagram

Fila de posts semanais do @managecode, publicados pela API oficial do Instagram às terças e quintas às 11h40 (só publica nos dias que estão na agenda) (horário de Brasília).

| Data | Post | Tema | Onde está a arte |
|---|---|---|---|
| ter 01/12/2026 | post-10 | Quanto custa uma tarefa manual? | JPG no repo · Canva DAHb4AypOS0 |
| ter 08/12/2026 | post-11 | 5 perguntas antes de contratar | JPG no repo · Canva DAHb4F14VIM |
| ter 15/12/2026 | post-12 | Checklist de fim de ano | JPG no repo · Canva DAHb4LFMf74 |
| ter 22/12/2026 | post-13 | Planejando 2027 | JPG no repo · Canva DAHb4JzTvFI |
| qui 24/12/2026 | natal-2026 | Feliz Natal | JPG no repo · Canva DAHb4N0Wt9s |
| ter 29/12/2026 | post-14 | Sistema pronto ou sob medida? | JPG no repo · Canva DAHb4Kprzz8 |
| qui 31/12/2026 | ano-novo-2027 | Feliz Ano Novo | JPG no repo · Canva DAHb4NUV6Lg |
| ter 05/01/2027 | post-15 | 3 mitos sobre IA no WhatsApp | JPG no repo · Canva DAHb4B0Vo10 |

Os posts 01 a 09 já foram publicados (o 09 em 24/11/2026) e ficam aqui só como arquivo.

As artes foram exportadas do Canva em 24/11/2026 e estão em `posts/<post>/NN.jpg`; `canva_origem` na agenda aponta o design de origem. Se editar uma arte no Canva, exporte de novo e substitua os JPGs aqui, senão a versão antiga é a que sai.

Para adicionar um post: crie `posts/post-16/` com `01.jpg`, `02.jpg`… (1080×1350) e `legenda.txt`, e acrescente a data em `agenda.json`.

```bash
IG_TOKEN=... python3 publicar.py --teste   # confere sem publicar
IG_TOKEN=... python3 publicar.py           # publica o post de hoje
```

O token nunca fica neste repositório.
