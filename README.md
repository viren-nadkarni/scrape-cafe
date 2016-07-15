# scrape-cafe

A thingy to broadcast application decisions from GradCafe to a Telegram channel

[telegram.me/scrapecafe](https://telegram.me/scrapecafe)

- Keywords to search for are declared in `scrapecafe/spiders/gradcafe.py`
- The Telegram bot API key is to be declared in `scrapecafe/tokens.py`. Ask the [Botfather](https://core.telegram.org/bots#6-botfather) to create one for you.
- Make sure the channel name is also updated in `scrapecafe/pipelines.py`
