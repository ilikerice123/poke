package main

import (
	"crypto/subtle"
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

//ListDevices lists all the devices
func ListDevices(w http.ResponseWriter, r *http.Request) {
	if !BasicAuth(w, r) {
		return
	}

	ids := store.ListIDs()
	json.NewEncoder(w).Encode(map[string]interface{}{
		"ids": ids,
	})
}

func handleError(w http.ResponseWriter, err *store.Err) {
	switch err.Code {
	case store.NotFound:
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "device not found",
		})
	}
}

//BasicAuth returns True if authorized, and false otherwise, depends on User and Auth variable
func BasicAuth(w http.ResponseWriter, r *http.Request) bool {
	user, pass, ok := r.BasicAuth()

	if !ok || subtle.ConstantTimeCompare([]byte(user), []byte(User)) != 1 || subtle.ConstantTimeCompare([]byte(pass), []byte(Pass)) != 1 {
		w.Header().Set("WWW-Authenticate", `Basic realm="Provide User and Pass"`)
		w.WriteHeader(401)
		w.Write([]byte("Unauthorised.\n"))
		return false
	}

	return true
}
