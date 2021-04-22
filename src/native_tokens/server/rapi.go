package main
 
import (
	"encoding/json"
	"net/http"
	"fmt"
)
 
type NFT struct {
	Id          integer `json:"Id"`
	Title       string `json:"Title"`
	StorageLink string `json:"Storage"`
	Name   string `json:"Text"`
}
 
func PostsHandler(w http.ResponseWriter, r *http.Request) {
 
    nfts := []NFT{
        NFT{"Post one", "John", "This is first post."},
        NFT{"Post two", "Jane", "This is second post."},
        NFT{"Post three", "John", "This is another post."},
    }
 
    json.NewEncoder(w).Encode(posts)
}
 
func main() {
	
	fmt.Println("Starting a server on localhost:5051")
	http.HandleFunc("/posts", PostsHandler)
	http.ListenAndServe(":5051", nil)
}
