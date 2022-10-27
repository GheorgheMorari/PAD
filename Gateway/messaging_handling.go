package main

import "net/http"

type MessagingServiceEntrypoint struct {
	entrypoint string
}

const messagingServiceName = "MessagingService"

var messagingServiceStore *ServiceStore = nil

func (messagingServiceEntrypoint MessagingServiceEntrypoint) messagingServiceFw(w http.ResponseWriter, req *http.Request) {
	if messagingServiceStore == nil {
		http.Error(w, "Messaging service is unavailable", http.StatusInternalServerError)
		return
	}
	messagingServiceStore.forward(w, req, messagingServiceEntrypoint.entrypoint)
	println("Forwarded to " + messagingServiceEntrypoint.entrypoint)
}

func messagingServiceHandlingMain() {
	http.HandleFunc("/send_message", MessagingServiceEntrypoint{"send_message"}.messagingServiceFw)
	http.HandleFunc("/get_messages", MessagingServiceEntrypoint{"get_messages"}.messagingServiceFw)
}
