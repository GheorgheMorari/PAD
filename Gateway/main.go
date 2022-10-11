package main

import (
	"io"
	"net/http"
)

const gatewayHost = "127.0.0.1"
const gatewayPort = "8080"

type ServiceStore struct {
	services    []string
	serviceName string
}

var globalClient http.Client
var serviceTypeAddressMap map[string]ServiceStore

func (serviceStore *ServiceStore) forward(w http.ResponseWriter, req *http.Request) {
	currentService := serviceStore.services[0] // TODO choose service based on workload
	request, newRequestErr := http.NewRequest(http.MethodPost, currentService, req.Body)
	if newRequestErr != nil {
		http.Error(w, "Could not create new request for service:"+serviceStore.serviceName, http.StatusInternalServerError)
		return
	}
	response, doErr := globalClient.Do(request)
	if doErr != nil {
		http.Error(w, "Could not send request for service:"+serviceStore.serviceName, http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", response.Header.Get("Content-Type"))
	w.Header().Set("Content-Length", response.Header.Get("Content-Length"))
	io.Copy(w, response.Body)
	response.Body.Close()
}

func handle(w http.ResponseWriter, req *http.Request) {
	//TODO parse request
	//TODO choose necessary service
	//TODO choose the least busy service provider
	//TODO send the request to that service
	//TODO respond with the response from the service provider
}

func main() {
	serviceTypeAddressMap = make(map[string]ServiceStore)
	discoveryCommMain()

	http.HandleFunc("/", handle)
	_ = http.ListenAndServe("http://"+gatewayHost+":"+gatewayPort, nil)
}
