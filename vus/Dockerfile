ARG BUILD_FROM

FROM $BUILD_FROM
WORKDIR /root/
ADD entrypoint.sh entrypoint.sh
ENTRYPOINT [ "/usr/bin/env", "bashio" ]
CMD [ "entrypoint.sh" ]