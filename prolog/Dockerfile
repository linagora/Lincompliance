FROM swipl:latest

WORKDIR /app

COPY --chmod=755 . .

EXPOSE 8888

ENTRYPOINT ["swipl"]
CMD ["/app/server.pl",  "--user=daemon", "--fork=false", "--port=8888"]