# scrape-cafe

A thingy to broadcast application decisions from GradCafe to a Telegram channel

[telegram.me/scrapecafe](https://telegram.me/scrapecafe)

### Configuration

Configuration is handled by `settings.py`

- `KEYWORDS`: Declare the keywords to search GradCafe
- `TELEGRAM_BOT_API_KEY`: Specify the Telegram bot API key. Ask the [BotFather](https://core.telegram.org/bots#6-botfather) to create one for you.
- `TELEGRAM_CHANNEL_NAME`: Set the channel name where updates will be broadcasted. Channel names start with a `@`

### Usage

Create a cron job to run the crawler periodically, like every 5 minutes:

    */5 * * * * cd ~/scrape-cafe && /usr/local/bin/scrapy crawl gradcafe

---

License: MIT
