package main
 
import (
	"encoding/json"
	"net/http"
	"fmt"
)

type NFTMeta struct {
	keywords   string `json:"keywords"`
	image      string `json:"image"`
	version    string `json:"version"`
	copyright  string `json:"copyright"`
}


type NftToken struct {
	policyid    string  `json:"policyid"`
	assetName   string  `json:"assetName"`
	assetAmount integer `json:"assetAmount"`
	mintingCost float   `json:"mintingCost"`
	recvAddr    string  `json:"recvAddr"`
	metaInfo    NFTMeta `json:"NftMeta"`
}

 
func PostsHandler(w http.ResponseWriter, r *http.Request) {

	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		fmt.Fprintf(w, "invalid_http_method")
		return
	}

	// Must call ParseForm() before working with data
	r.ParseForm()

	// Log all data. Form is a map[]
	log.Println(r.Form)

	// Print the data back. We can use Form.Get() or Form["name"][0]
	fmt.Fprintf(w, r.Form.Get("policyid"))


	//Check all the parameters and then invoke the python code for the blockchain code.
	
	
}



func main() {
	
	fmt.Println("Starting a server on localhost:5051")
	http.HandleFunc("/nfts", PostsHandler)
	http.ListenAndServe(":5051", nil)
}
