ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add minidlna
#RUN install -Dm644 /etc/minidlna.conf ~/.config/minidlna/minidlna.conf

WORKDIR /

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]