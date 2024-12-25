FROM python:3.12.8

WORKDIR /client

COPY ./requirements.txt /client/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /client/requirements.txt

COPY . /client/

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["client.py"]
