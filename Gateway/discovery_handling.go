package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

type DiscoveryServiceOutput struct {
	ServiceName string `json:"serviceName"`
	FullAddress string `json:"fullAddress"`
}

func updateServices() {
	serviceStoreMap = make(map[string]*ServiceStore)

	request, newRequestErr := http.NewRequest(http.MethodPost, discoveryHost+":"+discoveryPort, nil)
	if newRequestErr != nil {
		panic("Could not create a request to discovery service")
	}
	response, doErr := globalClient.Do(request)
	if doErr != nil {
		log.Fatal(doErr)
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
	authServiceStore = serviceStoreMap[authServiceName]
	println("Services updated")

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
