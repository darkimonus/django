FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=network.network.settings

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN echo "Before COPY:" && ls -lah /app
COPY ./network/ /app
COPY docker-entrypoint.sh /
RUN echo "After COPY:" && ls -lah /app

RUN pip install -r requirements.txt
RUN chmod 755 /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
