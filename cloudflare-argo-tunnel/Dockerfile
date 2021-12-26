ARG BUILD_FROM
FROM $BUILD_FROM AS builder

WORKDIR /tmp
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH /go/bin:$PATH
RUN apk add --no-cache git make musl-dev go
RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin && go get -d -v github.com/cloudflare/cloudflared

FROM $BUILD_FROM
WORKDIR /root/
COPY --from=builder /go/src/github.com/cloudflare/cloudflared/cloudflared ./
ENTRYPOINT [ "./cloudflared" ]
CMD [ "origincert", "/data/cert.pem", "config", "/data/config.yaml" ]