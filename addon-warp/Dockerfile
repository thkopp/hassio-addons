ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache g++ make linux-headers git
# RUN apk update
# RUN apk add make
# RUN apk add gcc
# RUN apk add linux-headers
# RUN apk add git
RUN git clone https://github.com/nikp123/wake-on-arp.git /wake-on-arp.git
WORKDIR /wake-on-arp.git
RUN make
RUN make install

# Copy data for add-on
# COPY wake-on-arp /usr/bin/wake-on-arp
# RUN chmod a+x /usr/bin/wake-on-arp
# COPY wake-on-arp /
# RUN chmod a+x /wake-on-arp

WORKDIR /

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]