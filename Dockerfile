FROM python:3.6.8-alpine3.8
#Installing essential packages
EXPOSE 9000

WORKDIR /mc/events_emitter/
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    && apk add python3-dev libxslt-dev libxml2-dev mysql-dev gcc musl-dev jpeg-dev zlib-dev mysql-client g++ \
    && apk add ca-certificates wget

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN apk del .build-deps

ADD . /mc/events_emitter/
RUN mv events_emitter/example-settings.py events_emitter/settings.py
RUN python manage.py collectstatic --no-input
RUN chmod +x ./run.sh

ENTRYPOINT ["./run.sh"]
CMD ["events_emitter"]
