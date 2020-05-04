package store

import (
	"fmt"
	"sync"
	"time"

	"github.com/google/uuid"
)

//ErrorCode represents error codes
type ErrorCode int

//Declares the constant error codes
const (
	NotFound ErrorCode = 0
)

//Err signifies store errors
type Err struct {
	Msg  string
	Code ErrorCode
}

func (err *Err) Error() string {
	return err.Msg
}

//Poke used to store status
type Poke struct {
	ID    string     `json:"id"`
	Cv    *sync.Cond `json:"-"`
	Poked bool       `json:"poke"`
}

//PokeStore stores pokes
var pokeStore map[string]*Poke

//Init inits the data store
//TODO: not sure if this is best pattern
func Init() {
	pokeStore = make(map[string]*Poke)
}

//NewPoke creates a new PokeStore
func NewPoke() *Poke {
	poke := &Poke{
		ID:    uuid.New().String(),
		Cv:    sync.NewCond(&sync.Mutex{}),
		Poked: false,
	}
	pokeStore[poke.ID] = poke
	return poke
}

//SendPoke sends a poke to the id
func SendPoke(id string) *Err {
	poke := pokeStore[id]
	if poke == nil {
		return &Err{Msg: "id not found", Code: NotFound}
	}

	fmt.Println("broadcasting on poke " + poke.ID)
	poke.Cv.Broadcast()
	poke.Poked = true
	time.AfterFunc(2*time.Second, func() {
		poke.Poked = false
	})

	return nil
}

//WaitPoke blocks until the specified id receives a poke
func WaitPoke(id string) (*Poke, *Err) {
	poke := pokeStore[id]
	if poke == nil {
		return nil, &Err{Msg: "id not found", Code: NotFound}
	}
	if poke.Poked == true {
		return poke, nil
	}

	fmt.Println("waiting on poke " + poke.ID)
	poke.Cv.L.Lock()
	poke.Cv.Wait()
	return poke, nil
}

//ListIDs lists the ids of all the devices
func ListIDs() []string {
	list := make([]string, len(pokeStore))

	i := 0
	for id := range pokeStore {
		list[i] = id
		i++
	}
	return list
}
