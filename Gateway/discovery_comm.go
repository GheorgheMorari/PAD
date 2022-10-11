package main

import (
	"encoding/json"
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
	serviceName string
	fullAddress string
}

func updateServices() {
	serviceTypeAddressMap = make(map[string]ServiceStore)

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
		if serviceStore, ok := serviceTypeAddressMap[serviceOutput.serviceName]; ok {
			serviceStore.services = append(serviceStore.services, serviceOutput.fullAddress)
		} else {
			serviceTypeAddressMap[serviceOutput.serviceName] = ServiceStore{serviceName: serviceOutput.serviceName, services: []string{serviceOutput.fullAddress}}
		}
	}
}
func updateServicesRoutine() {
	for true {
		updateServices()
		time.Sleep(UpdateServicesDelay)
	}
}

func discoveryCommMain() {
	if UpdateServicesRoutine {
		go updateServicesRoutine()
	} else {
		updateServices()
	}
}
