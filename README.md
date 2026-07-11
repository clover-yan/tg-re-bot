# tg-re-bot

## docker run

```bash
docker run -e BOT_TOKEN="your_token" ghcr.io/clover-yan/tg-re-bot
```

## docker compose

```yaml
services:
  bot:
    image: ghcr.io/clover-yan/tg-re-bot
    environment:
      - BOT_TOKEN=your_token
```
