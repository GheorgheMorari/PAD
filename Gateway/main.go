package main

import (
	"net/http"
)

//There are multiple services
//The services that the gateway can access are:
//- User storage service
//- Message storage service
//- Service discovery

func handle(w http.ResponseWriter, req *http.Request) {
	//TODO parse request
	//TODO choose necessary service
	//TODO choose the least busy service provider
	//TODO send the request to that service
	//TODO respond with the response from the service provider
}

func main() {
	http.HandleFunc("/", handle)
	_ = http.ListenAndServe(":8090", nil)
}
