# tg-re-bot

Repeats the message when you call it.

## Usage

Demo: [@the_re_bot](https://t.me/the_re_bot)

```text
[reply] /re@the_re_bot
```

## Run

### docker run

```bash
docker run -e BOT_TOKEN="your_token" --name tg-re-bot --restart unless-stopped ghcr.io/clover-yan/tg-re-bot:master
```

### docker compose

```yaml
services:
  tg-re-bot:
    image: ghcr.io/clover-yan/tg-re-bot:master
    container_name: tg-re-bot
    restart: unless-stopped
    environment:
      - BOT_TOKEN=your_token
```

```bash
docker compose up -d
```
