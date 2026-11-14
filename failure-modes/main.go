// A web service that fails in a chosen way, so a check can see how the
// platform reports each failure. One binary, its behaviour set by MODE:
//
//	ok     every path answers 200.
//	oom    GET /burst allocates and touches memory until the container
//	       runs out of memory; every other path answers 200.
//	oom-start allocates and touches memory at startup, before it listens,
//	       so the container runs out of memory on every start.
//	reset  every path but /healthz accepts the request, then closes the
//	       connection with no reply (TCP RST); /healthz answers 200.
//	refuse nothing listens on PORT; /healthz answers 200 on HEALTH_PORT
//	       (default 8081) only.
//
// It listens on PORT (default 8080). Nothing else: no secrets, no outbound
// calls, no storage.
package main

import (
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"time"
)

var hold [][]byte

func main() {
	mode := os.Getenv("MODE")
	if mode == "" {
		mode = "ok"
	}
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	if mode == "oom-start" {
		log.Printf("mode=oom-start: allocating until out of memory")
		burn()
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) {
		fmt.Fprintln(w, "ok")
	})
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		switch {
		case mode == "oom" && r.URL.Path == "/burst":
			burn()
		case mode == "reset":
			hj, ok := w.(http.Hijacker)
			if !ok {
				http.Error(w, "no hijack", http.StatusInternalServerError)
				return
			}
			conn, _, err := hj.Hijack()
			if err != nil {
				return
			}
			if tc, ok := conn.(*net.TCPConn); ok {
				_ = tc.SetLinger(0) // close with RST, not FIN
			}
			_ = conn.Close()
		default:
			fmt.Fprintf(w, "failure-modes %s\n", mode)
		}
	})
	// /healthz also answers on HEALTH_PORT when it is set (in every mode), so
	// a health check on that port passes whatever MODE is.
	hp := os.Getenv("HEALTH_PORT")
	if mode == "refuse" && hp == "" {
		hp = "8081"
	}
	if hp != "" {
		h := http.NewServeMux()
		h.HandleFunc("/healthz", func(w http.ResponseWriter, _ *http.Request) { fmt.Fprintln(w, "ok") })
		hs := &http.Server{Addr: ":" + hp, Handler: h, ReadHeaderTimeout: 10 * time.Second}
		if mode == "refuse" {
			log.Printf("mode=refuse health_port=%s, nothing on %s", hp, port)
			log.Fatal(hs.ListenAndServe())
		}
		go func() { log.Fatal(hs.ListenAndServe()) }()
	}
	srv := &http.Server{Addr: ":" + port, Handler: mux, ReadHeaderTimeout: 10 * time.Second}
	log.Printf("mode=%s port=%s", mode, port)
	log.Fatal(srv.ListenAndServe())
}

// burn allocates 32 MiB at a time and touches every page, so the memory is
// really used, until the process is killed for running out of it.
func burn() {
	for {
		b := make([]byte, 32<<20)
		for i := range b {
			if i%4096 == 0 {
				b[i] = 1
			}
		}
		hold = append(hold, b)
	}
}
