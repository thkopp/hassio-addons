ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache minidlna
#RUN install -Dm644 /etc/minidlna.conf ~/.config/minidlna/minidlna.conf

WORKDIR /data

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]