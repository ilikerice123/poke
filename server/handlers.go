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
	writeJSON(w, poke)
}

//PokeDevice pokes a device
func PokeDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	err := store.SendPoke(id)
	if err != nil {
		handleError(w, err)
		return
	}

	writeJSON(w, map[string]interface{}{"status": "ok"})
}

//CheckDevice checks a device for poke
func CheckDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	poke, err := store.WaitPoke(id)
	if err != nil {
		handleError(w, err)
		return
	}

	writeJSON(w, poke)
}

//ListDevices lists all the devices
func ListDevices(w http.ResponseWriter, r *http.Request) {
	if !basicAuth(w, r) {
		return
	}

	ids := store.ListIDs()
	writeJSON(w, map[string]interface{}{"ids": ids})
}

//ActivateDevice activates a poke device given a 6 digit numeric string
func ActivateDevice(w http.ResponseWriter, r *http.Request) {
	code := mux.Vars(r)["code"]
	poke, err := store.ActivatePoke(code)
	if err != nil {
		handleError(w, err)
		return
	}

	writeJSON(w, poke)
}

func handleError(w http.ResponseWriter, err *store.Err) {
	fmt.Println("Handling error")
	switch err.Code {
	case store.NotFound:
		writeJSON(w, map[string]interface{}{"status": "device not found"})
		w.WriteHeader(http.StatusNotFound)
	default:
		writeJSON(w, map[string]interface{}{"status": "server error"})
		w.WriteHeader(http.StatusInternalServerError)
	}
}

func basicAuth(w http.ResponseWriter, r *http.Request) bool {
	user, pass, ok := r.BasicAuth()

	if !ok || subtle.ConstantTimeCompare([]byte(user), []byte(User)) != 1 || subtle.ConstantTimeCompare([]byte(pass), []byte(Pass)) != 1 {
		w.Header().Set("WWW-Authenticate", `Basic realm="Provide User and Pass"`)
		w.WriteHeader(401)
		w.Write([]byte("Unauthorized.\n"))
		return false
	}

	return true
}

func writeJSON(w http.ResponseWriter, object interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(object)
}
