# Manage Code · Instagram

Fila de posts semanais do @managecode, publicados pela API oficial do Instagram toda terça às 11h40 (horário de Brasília).

| Data | Post | Tema |
|---|---|---|
| 01/12/2026 | post-09 | Três formas de começar |

Os posts 01 a 08 já foram publicados manualmente e ficam aqui só como arquivo.

Para adicionar um post: crie `posts/post-10/` com `01.jpg`, `02.jpg`… (1080×1350) e `legenda.txt`, e acrescente a data em `agenda.json`.

```bash
IG_TOKEN=... python3 publicar.py --teste   # confere sem publicar
IG_TOKEN=... python3 publicar.py           # publica o post de hoje
```

O token nunca fica neste repositório.
