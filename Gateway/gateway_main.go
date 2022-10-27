package main

import (
	"io"
	"net/http"
	"time"
)

const discoveryHost = "http://127.0.0.1"
const discoveryPort = "6969"

const UpdateServicesRoutine = false
const UpdateServicesDelay = 5 * time.Second

const gatewayPort = "8080"

type ServiceStore struct {
	addresses   []string
	serviceName string
}

var globalClient http.Client
var serviceStoreMap map[string]*ServiceStore

func (serviceStore *ServiceStore) forward(w http.ResponseWriter, req *http.Request, entrypoint string) {
	currentServiceAddress := serviceStore.addresses[0] // TODO choose service based on workload

	request, newRequestErr := http.NewRequest(http.MethodPost, currentServiceAddress+entrypoint, req.Body)
	if newRequestErr != nil {
		http.Error(w, "Could not create new request for service:"+serviceStore.serviceName, http.StatusInternalServerError)
		return
	}
	request.Header = req.Header.Clone()
	request.URL.RawQuery = req.URL.RawQuery
	for _, cookie := range req.Cookies() {
		request.AddCookie(cookie)
	}
	response, doErr := globalClient.Do(request)

	if doErr != nil {
		http.Error(w, "Could not send request for service:"+serviceStore.serviceName, http.StatusInternalServerError)
		panic(doErr)
	}

	response.Header.Clone()
	w.Header().Set("Content-Type", response.Header.Get("Content-Type"))
	w.Header().Set("Content-Length", response.Header.Get("Content-Length"))
	w.WriteHeader(response.StatusCode)
	_, err := io.Copy(w, response.Body)
	if err != nil {
		panic(err)
	}
	err = response.Body.Close()
	if err != nil {
		panic(err)
	}
}

func main() {
	serviceStoreMap = make(map[string]*ServiceStore)
	discoveryCommMain()
	authServiceHandlingMain()
	messagingServiceHandlingMain()

	println("Starting server at port:" + gatewayPort)
	err := http.ListenAndServe(":"+gatewayPort, nil)
	if err != nil {
		panic(err)
	}
}
