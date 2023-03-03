# TGBOT

Telegram bot that integrates both ChatGPT and BingAI, combining two different artificial intelligence technologies to provide a more comprehensive and accurate response.

### Table of Contents

- [TGBOT](#tgbot)
    - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Usage](#usage)
    - [Bot Commands](#bot-commands)
  - [Reporting Bugs and Issues](#reporting-bugs-and-issues)
  - [Contributing](#contributing)
  - [Support](#support)
  - [License](#license)
  - [Credits](#credits)
  - [Disclaimer](#disclaimer)
  - [Contact](#contact)

## Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/)

We use [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments. Please install it before proceeding.

### Setup

1. Clone the repository
  
2. Install the dependencies

```sh
poetry install
```

3. Create a new Telegram bot using [@BotFather](https://t.me/BotFather) and copy the token
4. Set the environment variables as mentioned in the [Environment Variables](#environment-variables) section
5. Run the bot with the following command, if you are developing the bot, you can use `poetry shell` to activate the virtual environment.

```sh
poetry run tgbot
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

## Usage

**Send any message to the bot to start a conversation with AI based on the current chat mode.**

*Reply to a message to continue the conversation with all the previous messages in the thread. Otherwise, the conversation will start from the beginning.*

### Bot Commands

| Command | Description |
| --- | --- |
| `/start` | Start the bot |
| `/help` | Get help |
| `/cm` | Get current chat mode |
| `/cm [mode]` | Set chat mode. Either `ChatGPT` as `gpt` (default) or `BingAI` as `bing` |
| `/ping` | Check if the bot is alive |
| `/echo [text]` | Echo the text |
| `/msginfo` | Get information about the message |
| `/del` | Delete any message with reply or message ID |
| `/info` | Get your user ID and chat ID |

## Reporting Bugs and Issues

If you find any bugs or issues, please report them by opening an issue.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you like this project, please consider donating with [GitHub Sponsors](https://github.com/sponsors/rabilrbl).

## License

[GNU AFFERO GENERAL PUBLIC LICENSE Version 3](LICENSE)

## Credits

- [ChatGPT](https://github.com/acheong08/ChatGPT) for the ChatGPT Integration.
- [EdgeGPT](https://github.com/acheong08/EdgeGPT) for the BingAI Integration.

## Disclaimer

This project is not affiliated with Telegram or OpenAI or Microsoft or any other company. This project is for educational purposes only. The author is not responsible for any misuse of this project. Use at your own risk. 

By using this project, you agree to the terms and conditions mentioned in the [License](LICENSE).

## Contact

- [Telegram](https://t.me/rabilrbl)
