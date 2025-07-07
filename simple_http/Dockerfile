FROM alpine:latest

RUN apk add --no-cache netcat-openbsd

COPY server.sh /server.sh
COPY index.html /index.html
RUN chmod +x /server.sh

CMD ["/server.sh"]