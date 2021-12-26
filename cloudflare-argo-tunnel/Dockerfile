ARG BUILD_FROM
FROM $BUILD_FROM AS builder

WORKDIR /tmp
RUN apt-get update && apt-get -y install golang
RUN go get -d -v github.com/cloudflare/cloudflared

FROM $BUILD_FROM
WORKDIR /root/
COPY --from=builder /go/src/github.com/cloudflare/cloudflared/cloudflared ./
ENTRYPOINT [ "./cloudflared" ]