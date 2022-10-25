package main

import (
	"net/http"
)

const authServiceName = "AuthService"

var authServiceStore *ServiceStore = nil

type AuthServiceEntrypoint struct {
	entrypoint string
}

func (authServiceEntrypoint AuthServiceEntrypoint) authServiceFw(w http.ResponseWriter, req *http.Request) {
	if authServiceStore == nil {
		http.Error(w, "Auth service store is unavailable", http.StatusInternalServerError)
		return
	}
	authServiceStore.forward(w, req, authServiceEntrypoint.entrypoint)
	println("Forwarded to " + authServiceEntrypoint.entrypoint)
}

func authServiceHandlingMain() {
	http.HandleFunc("/login", AuthServiceEntrypoint{"api/auth/login"}.authServiceFw)
	http.HandleFunc("/register", AuthServiceEntrypoint{"api/auth/register"}.authServiceFw)
	http.HandleFunc("/refresh", AuthServiceEntrypoint{"api/auth/refresh"}.authServiceFw)
	http.HandleFunc("/logout", AuthServiceEntrypoint{"api/auth/logout"}.authServiceFw)
	http.HandleFunc("/me", AuthServiceEntrypoint{"api/users/me"}.authServiceFw)
}
