package main

import (
	"fmt"

	"github.com/gorilla/mux"
	"github.com/ilikerice123/poke/server/store"
)

func main() {
	store.Init()
	fmt.Println("Hello World!!")

	r := mux.NewRouter()

	deviceRouter := mux.NewRouter()
	r.Handle("/device", deviceRouter)

	deviceRouter.HandleFunc("/", NewDevice).Methods("POST")
	deviceRouter.HandleFunc("{id}/poke", PokeDevice).Methods("POST")
	deviceRouter.HandleFunc("{id}/poke", CheckDevice).Methods("GET")
}
