FROM golang:1.18
WORKDIR $GOPATH/src

COPY . .

EXPOSE 8080


RUN go mod download
RUN go build -o /main

CMD ["/main"]