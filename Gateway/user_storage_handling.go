package main

import (
	"net/http"
)

const userStorageServiceName = "UserStorage"

var userStorageServiceStore *ServiceStore = nil

type UserStorageServiceEntrypoint struct {
	entrypoint string
}

func (userStorageEntrypoint UserStorageServiceEntrypoint) userStorageServiceFw(w http.ResponseWriter, req *http.Request) {
	if userStorageServiceStore == nil {
		http.Error(w, "User storage service store is unavailable", http.StatusInternalServerError)
		return
	}
	userStorageServiceStore.forward(w, req, userStorageEntrypoint.entrypoint)
	println("Forwarded to " + userStorageEntrypoint.entrypoint)
}

func userStorageHandlingMain() {
	http.HandleFunc("/login", UserStorageServiceEntrypoint{"api/auth/login"}.userStorageServiceFw)
	http.HandleFunc("/register", UserStorageServiceEntrypoint{"api/auth/register"}.userStorageServiceFw)
	http.HandleFunc("/refresh", UserStorageServiceEntrypoint{"api/auth/refresh"}.userStorageServiceFw)
	http.HandleFunc("/logout", UserStorageServiceEntrypoint{"api/auth/logout"}.userStorageServiceFw)
	http.HandleFunc("/me", UserStorageServiceEntrypoint{"api/users/me"}.userStorageServiceFw)
}
