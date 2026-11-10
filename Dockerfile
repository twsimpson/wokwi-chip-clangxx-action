FROM alpine:3.21

RUN apk update && \
    apk add clang llvm lld git make cmake ninja-build curl libc++-dev wasi-sdk

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]