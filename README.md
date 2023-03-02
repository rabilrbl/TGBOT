# TGBOT

Telegram bot that integrates both ChatGPT and BingAI, combining two different artificial intelligence technologies to provide a more comprehensive and accurate response to user queries.

## Installation

### Prerequisites

- Python 3.11+
- Pip or any other package manager for Python

### Setup

1. Clone the repository
  
2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Create a new Telegram bot using [@BotFather](https://t.me/BotFather) and copy the token
4. Set the environment variables as mentioned in the [Environment Variables](#environment-variables) section
5. Run the bot

```bash
python3 main.py
```

## Environment Variables

| Name | Description | Required |
| --- | --- | --- |
| `API_HASH` | API hash for your Telegram account. Get it from [here](https://my.telegram.org/apps) by creating a new app | Yes |
| `API_ID` | API ID for your Telegram account. Available in the same page as API hash | Yes |
| `AUTHORIZED_USERS` | Comma-separated list of Telegram usernames that are authorized to use the bot | Yes |
| `BING_COOKIES` | Bing cookies copied from cookie editor extension in browsers. **You must have access to the new Bing Chat** | Yes |
| `BOT_TOKEN` | Telegram bot token | Yes |
| `OPENAI_EMAIL` | OpenAI account email address. *This does not work with google or microsoft accounts*. | Yes |
| `OPENAI_PASSWORD` | OpenAI account password | Yes |


## Reporting Bugs and Issues

If you find any bugs or issues, please report them by opening an issue.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you like this project, please consider donating with [GitHub Sponsors](https://github.com/sponsors/rabilrbl).

## License

[GNU AFFERO GENERAL PUBLIC LICENSE Version 3](LICENSE)

## Credits

- [ChatGPT](https://github.com/acheong08/ChatGPT) by @acheong08
- [EdgeGPT](https://github.com/acheong08/EdgeGPT) by @acheong08

## Disclaimer

This project is not affiliated with Telegram or OpenAI or Microsoft or any other company. This project is for educational purposes only. The author is not responsible for any misuse of this project. Use at your own risk. 

By using this project, you agree to the terms and conditions mentioned in the [License](LICENSE).

## Contact

- [Telegram](https://t.me/rabilrbl)
