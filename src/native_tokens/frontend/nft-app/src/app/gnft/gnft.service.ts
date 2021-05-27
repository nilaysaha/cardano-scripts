import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { NFT } from './gnft';

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})


export class NftService {

    private ApiUrl: string = "https://nft.oef.io/api/nft";

    constructor(private http:HttpClient) {
	
    }
    
    createNft(nftModel: NFT ) {
	const headers = { 'content-type': 'application/json'}  
        let body = JSON.stringify(nftModel);
	console.log(`Now posting to url:${this.ApiUrl} the data:`)
	console.log(body)
	console.log(httpOptions)
        return this.http.post(this.ApiUrl, body, {'headers':headers});
    }

}
