FROM alpine:latest

RUN apk add --no-cache bash tzdata coreutils

ENV TZ=UTC

WORKDIR /app

COPY logger.sh .

ENTRYPOINT [ "./logger.sh" ]