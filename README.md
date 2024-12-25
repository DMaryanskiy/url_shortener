# URL Shortener service

Small API which helps to shorten your enourmous big url to a moew tiny one.
Just put your url in a form and it'll generate small uri for it.
Also you may provide your own uri to get your custom link.
If short link already exists for a long url, we'll send you existing link

## Installation

1. Clone repo
2. Create `.env` file with two variables:
    ```.env
    SQLITE_FILE_NAME=<name of your sqlite DB>
    DOMAIN=<your domain e.g. https://example.com:port>
    ```
3. Run a command `docker-compose up --build`
4. Enjoy!

## Hall of badges

[![python](https://img.shields.io/badge/Python-3.12.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

