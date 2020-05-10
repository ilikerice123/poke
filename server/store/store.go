package store

import (
	"crypto/rand"
	"io"
	"sync"
	"time"

	"github.com/google/uuid"
)

//ErrorCode represents error codes
type ErrorCode int

//Declares the constant error codes
const (
	NotFound      ErrorCode = 1
	NumCodeDigits int       = 6
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
	ID     string     `json:"id"`
	Cv     *sync.Cond `json:"-"`
	Poked  bool       `json:"poked"`
	Active bool       `json:"active"`
	Code   string     `json:"code"`
}

//PokeStore stores pokes
var pokeStore map[string]*Poke

//tempStore stores pokes that need to be activated
var tempStore map[string]*Poke

//Init inits the data store
//TODO: not sure if this is best pattern
func Init() {
	pokeStore = make(map[string]*Poke)
	tempStore = make(map[string]*Poke)
}

//NewPoke creates a new PokeStore, and sets a timeout logic
func NewPoke() *Poke {
	poke := &Poke{
		ID:     uuid.New().String(),
		Cv:     sync.NewCond(&sync.Mutex{}),
		Poked:  false,
		Active: false,
		Code:   randCode(),
	}
	pokeStore[poke.ID] = poke
	tempStore[poke.Code] = poke
	time.AfterFunc(1*time.Hour, func() { timeoutPoke(poke.ID) })
	return poke
}

//ActivatePoke activates a poke and returns the uuid
func ActivatePoke(code string) (*Poke, *Err) {
	poke := tempStore[code]
	if poke == nil || poke.Active {
		return nil, &Err{Msg: "code not found", Code: NotFound}
	}
	poke.Active = true
	poke.Cv.L.Lock()
	poke.Cv.Broadcast()
	poke.Cv.L.Unlock()
	delete(tempStore, code)
	return poke, nil
}

//WaitActivation waits for a poke to be activated
func WaitActivation(id string) (*Poke, *Err) {
	poke := pokeStore[id]
	if poke == nil {
		return nil, &Err{Msg: "id not found", Code: NotFound}
	}
	poke.Cv.L.Lock()
	defer poke.Cv.L.Unlock()
	if poke.Active {
		return poke, nil
	}
	poke.Cv.Wait()
	return poke, nil
}

//SendPoke sends a poke to the id
func SendPoke(id string) *Err {
	poke := pokeStore[id]
	if poke == nil || !poke.Active {
		return &Err{Msg: "id not found", Code: NotFound}
	}

	poke.Poked = true
	poke.Cv.L.Lock()
	poke.Cv.Broadcast()
	poke.Cv.L.Unlock()
	time.AfterFunc(2*time.Second, func() {
		poke.Poked = false
	})

	return nil
}

//WaitPoke blocks until the specified id receives a poke
func WaitPoke(id string) (*Poke, *Err) {
	poke := pokeStore[id]
	if poke == nil || !poke.Active {
		return nil, &Err{Msg: "id not found", Code: NotFound}
	}
	if poke.Poked == true {
		return poke, nil
	}

	poke.Cv.L.Lock()
	poke.Cv.Wait()
	poke.Cv.L.Unlock()
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

//timeoutPoke removes a poke after a certain amount of time elapsed
//and the poke is not activated
func timeoutPoke(id string) {
	poke := pokeStore[id]
	if poke == nil || poke.Active {
		//lol it shouldn't be nil but whatever
		return
	}

	//broadcast to anyone waiting on activation
	poke.Cv.Broadcast()
	delete(pokeStore, id)
	delete(tempStore, poke.Code)
}

var table = []byte{'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

//randCode returns a 6 digit numeric string
func randCode() string {
	b := make([]byte, NumCodeDigits)
	io.ReadAtLeast(rand.Reader, b, NumCodeDigits)

	for i := 0; i < len(b); i++ {
		b[i] = table[int(b[i])%len(table)]
	}
	return string(b)
}
