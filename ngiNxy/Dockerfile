FROM nginx:mainline-alpine
WORKDIR /usr/local/bin
COPY reload.sh .
RUN chmod +x reload.sh
ENTRYPOINT reload.sh