FROM python:3.10.10-slim-bullseye AS build
ENV JAVA_HOME /usr/lib/jvm/java-1.11.0-openjdk-amd64

WORKDIR /app

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends git openjdk-11-jre-headless && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/spidasoftware/format.git

COPY wrapper.py .

FROM scratch
COPY --from=build / /
ENV JAVA_HOME /usr/lib/jvm/java-1.11.0-openjdk-amd64
WORKDIR /src
ENTRYPOINT [ "/app/wrapper.py" ]