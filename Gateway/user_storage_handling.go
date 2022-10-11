package main

import (
	"net/http"
)

const userStorageServiceName = "UserStorage"

var userStorageServiceStore *ServiceStore = nil

func userStorageServiceFw(w http.ResponseWriter, req *http.Request) {
	if userStorageServiceStore == nil {
		http.Error(w, "User storage service store is unavailable", http.StatusInternalServerError)
		return
	}
	userStorageServiceStore.forward(w, req)
}

func userStorageHandlingMain() {
	http.HandleFunc("/login", userStorageServiceFw)
	http.HandleFunc("/getUserVal", userStorageServiceFw)
	http.HandleFunc("/setUserVal", userStorageServiceFw)
}
