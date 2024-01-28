ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache g++ make linux-headers git moreutils
RUN git clone https://github.com/nikp123/wake-on-arp.git /wake-on-arp.git
WORKDIR /wake-on-arp.git
RUN make
RUN make install

WORKDIR /

COPY run.sh /
RUN chmod a+x /run.sh

RUN apk del g++ make linux-headers git
RUN rm -rf /wake-on-arp.git

CMD [ "/run.sh" ]