package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const discoveryHost = "127.0.0.1"
const discoveryPort = "6969"
const discoveryProtocol = "http://"

const UpdateServicesRoutine = false
const UpdateServicesDelay = time.Second

type DiscoveryServiceOutput struct {
	ServiceName string `json:"serviceName"`
	FullAddress string `json:"fullAddress"`
}

func updateServices() {
	serviceStoreMap = make(map[string]*ServiceStore)

	request, newRequestErr := http.NewRequest(http.MethodPost, discoveryProtocol+discoveryHost+":"+discoveryPort+"/", nil)
	if newRequestErr != nil {
		panic("Could not create a request to discovery service")
	}
	response, doErr := globalClient.Do(request)
	if doErr != nil {
		panic("Could not sent request to discovery service")
	}
	var serviceOutputs []DiscoveryServiceOutput
	data, err := io.ReadAll(response.Body)
	if err != nil {
		panic("Could not read discovery service response body")
	}
	err = json.Unmarshal(data, &serviceOutputs)
	if err != nil {
		panic("Could not parse discovery service response")
	}
	for _, serviceOutput := range serviceOutputs {
		if serviceStore, ok := serviceStoreMap[serviceOutput.ServiceName]; ok {
			serviceStore.addresses = append(serviceStore.addresses, serviceOutput.FullAddress)
		} else {
			serviceStoreMap[serviceOutput.ServiceName] = &ServiceStore{serviceName: serviceOutput.ServiceName, addresses: []string{serviceOutput.FullAddress}}
		}
	}
	userStorageServiceStore = serviceStoreMap[userStorageServiceName]
	//TODO add the other services
}
func updateServicesRoutine() {
	for true {
		updateServices()
		time.Sleep(UpdateServicesDelay)
	}
}

func discoveryHandler(w http.ResponseWriter, req *http.Request) {
	updateServices()
	fmt.Fprintf(w, "OK")
}

func discoveryCommMain() {
	http.HandleFunc("/discover", discoveryHandler)

	if UpdateServicesRoutine {
		go updateServicesRoutine()
	} else {
		updateServices()
	}
}
