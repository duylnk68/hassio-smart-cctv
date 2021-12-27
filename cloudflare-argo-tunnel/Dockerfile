ARG BUILD_FROM
FROM golang:latest AS builder
WORKDIR /tmp
RUN git clone https://github.com/cloudflare/cloudflared.git
WORKDIR /tmp/cloudflared
RUN make cloudflared

FROM $BUILD_FROM
WORKDIR /root/
COPY --from=builder /tmp/cloudflared/cloudflared ./
ADD entrypoint.sh entrypoint.sh
ENTRYPOINT [ "/usr/bin/env", "bashio" ]
CMD [ "entrypoint.sh" ]