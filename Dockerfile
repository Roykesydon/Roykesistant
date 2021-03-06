FROM python:3.9.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 11539

CMD python main.py