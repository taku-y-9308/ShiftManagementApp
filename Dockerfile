FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV EMAIL_HOST_PASSWORD ${EMAIL_HOST_PASSWORD}

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod -R 755 .

CMD [ "./startup.sh" ]