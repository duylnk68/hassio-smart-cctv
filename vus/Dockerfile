ARG BUILD_FROM

FROM $BUILD_FROM
RUN apt update && apt install -y libicu
WORKDIR /root/
ADD entrypoint.sh entrypoint.sh
ENTRYPOINT [ "/usr/bin/env", "bashio" ]
CMD [ "entrypoint.sh" ]