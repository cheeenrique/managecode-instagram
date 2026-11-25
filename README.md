# Manage Code · Instagram

Fila de posts semanais do @managecode, publicados pela API oficial do Instagram toda terça às 11h40 (horário de Brasília).

| Data | Post | Tema |
|---|---|---|
| 01/12/2026 | post-01 | Apresentação |
| 08/12/2026 | post-02 | 6 sinais de que sua tecnologia ficou para trás |
| 15/12/2026 | post-03 | O método em quatro etapas |
| 22/12/2026 | post-04 | Um site para cada momento |
| 29/12/2026 | post-05 | 5 compromissos com cada cliente |
| 05/01/2027 | post-06 | Quem está por trás |
| 12/01/2027 | post-07 | IA no WhatsApp |
| 19/01/2027 | post-08 | Da planilha ao sistema |
| 26/01/2027 | post-09 | Três formas de começar |

Para adicionar um post: crie `posts/post-10/` com `01.jpg`, `02.jpg`… (1080×1350) e `legenda.txt`, e acrescente a data em `agenda.json`.

```bash
IG_TOKEN=... python3 publicar.py --teste   # confere sem publicar
IG_TOKEN=... python3 publicar.py           # publica o post de hoje
```

O token nunca fica neste repositório.
