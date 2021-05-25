import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
 
const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})



export class NftService {

    private ApiUrl: string = "https://nft.oef.io/api/nft";

    constructor(private http:HttpClient) {}
    
    createNft(nftModel) {
        let body = JSON.stringify(nftModel);
	console.log("Now posting the data")
	console.log(body)
        return this.http.post(this.ApiUrl, body, httpOptions);
    }

}
