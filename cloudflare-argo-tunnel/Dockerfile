ARG BUILD_FROM
FROM golang:alpine AS builder
RUN apk add --no-cache git make
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
