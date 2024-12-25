FROM python:3.12.8

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src/

EXPOSE 80

CMD ["fastapi", "run", "./main.py", "--port", "80"]
