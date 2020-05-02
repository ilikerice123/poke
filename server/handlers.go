package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/ilikerice123/poke/server/store"
)

//NewDevice creates a new poke device
func NewDevice(w http.ResponseWriter, r *http.Request) {
	poke := store.NewPoke()
	json.NewEncoder(w).Encode(poke)
}

//PokeDevice pokes a device
func PokeDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	fmt.Println(id)
	err := store.SendPoke(id)
	if err != nil {
		handleError(w, err)
		return
	}

	json.NewEncoder(w).Encode(map[string]interface{}{
		"status": "ok",
	})
	return
}

//CheckDevice checks a device for poke
func CheckDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	fmt.Println(id)
	poke, err := store.WaitPoke(id)
	if err != nil {
		handleError(w, err)
	}

	json.NewEncoder(w).Encode(poke)
	return
}

func handleError(w http.ResponseWriter, err *store.Err) {
	switch err.Code {
	case store.NotFound:
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "device not found",
		})
	}
}
