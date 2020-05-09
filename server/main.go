package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	"github.com/ilikerice123/poke/server/store"
)

//User string for username
var User string

//Pass string for password
var Pass string

func main() {
	User = os.Args[1]
	Pass = os.Args[2]

	store.Init()
	fmt.Println("Hello World!!")

	r := mux.NewRouter()

	deviceRouter := r.PathPrefix("/devices").Subrouter()
	deviceRouter.HandleFunc("/{id}/poke", PokeDevice).Methods("POST")
	deviceRouter.HandleFunc("/{id}/poke", CheckDevice).Methods("GET")
	deviceRouter.HandleFunc("/{code}/activate", ActivateDevice).Methods("POST")
	deviceRouter.HandleFunc("", NewDevice).Methods("POST")
	deviceRouter.HandleFunc("", ListDevices).Methods("GET")
	deviceRouter.HandleFunc("/", NewDevice).Methods("POST")
	deviceRouter.HandleFunc("/", ListDevices).Methods("GET")

	srv := &http.Server{
		Handler: r,
		Addr:    ":8000",
		// Good practice: enforce timeouts for servers you create!
		WriteTimeout: 24 * time.Hour,
		ReadTimeout:  24 * time.Hour,
	}
	log.Fatal(srv.ListenAndServe())
	wait := make(chan int, 1)
	<-wait
}
