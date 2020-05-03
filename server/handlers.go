package main

import (
	"crypto/subtle"
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/ilikerice123/poke/server/store"
)

//NewDevice creates a new poke device
func NewDevice(w http.ResponseWriter, r *http.Request) {
	poke := store.NewPoke()
	writeJSON(poke, w)
}

//PokeDevice pokes a device
func PokeDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	err := store.SendPoke(id)
	if err != nil {
		handleError(w, err)
		return
	}

	writeJSON(map[string]interface{}{"status": "ok"}, w)
}

//CheckDevice checks a device for poke
func CheckDevice(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	poke, err := store.WaitPoke(id)
	if err != nil {
		handleError(w, err)
	}

	writeJSON(poke, w)
}

//ListDevices lists all the devices
func ListDevices(w http.ResponseWriter, r *http.Request) {
	if !basicAuth(w, r) {
		return
	}

	ids := store.ListIDs()
	writeJSON(map[string]interface{}{"ids": ids}, w)
}

func handleError(w http.ResponseWriter, err *store.Err) {
	switch err.Code {
	case store.NotFound:
		writeJSON(map[string]interface{}{"status": "device not found"}, w)
		w.WriteHeader(http.StatusNotFound)
	default:
		writeJSON(map[string]interface{}{"status": "server error"}, w)
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

func writeJSON(object interface{}, w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(object)
}
