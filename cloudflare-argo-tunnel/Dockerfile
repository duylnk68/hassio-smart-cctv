ARG BUILD_FROM
FROM golang:latest AS builder
RUN go get -d -v github.com/cloudflare/cloudflared/cmd/cloudflared

FROM $BUILD_FROM
WORKDIR /root/
COPY --from=builder /go/bin/cloudflared ./
ENTRYPOINT [ "./cloudflared" ]
CMD [ "origincert", "/data/cert.pem", "config", "/data/config.yaml" ]