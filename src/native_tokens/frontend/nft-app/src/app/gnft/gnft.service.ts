import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable,  throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';

import { NFT } from './gnft';

const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'multipart/form-data' })
};

@Injectable({
  providedIn: 'root'
})


export class NftService {

    private ApiUrl: string = "https://nft.oef.io/api";
    private nftID: any;
    
    constructor(private http:HttpClient) {	
    }
   
    private handleError(error: HttpErrorResponse) {
	if (error.status === 0) {
	    // A client-side or network error occurred. Handle it accordingly.
	    console.error('An error occurred:', error.error);
	} else {
	    // The backend returned an unsuccessful response code.
	    // The response body may contain clues as to what went wrong.
	    console.error(`Backend returned code ${error.status}, ` +
		    `body was: ${error.error}`);
	}
	// Return an observable with a user-facing error message.
	return throwError(
	    'Something bad happened; please try again later.');
    }
    
    createNft(nftModel: NFT )  {
	const headers = {'Access-Control-Allow-Origin': '*'}
	
	let body = JSON.stringify(nftModel);

	console.log(`Now posting to url:${this.ApiUrl} the data:`)
	console.log(body)
	console.log(headers)

        return this.http.post<any>(this.ApiUrl+"/nft", nftModel, {'headers':headers})
    }

    uploadFile(file: File) {
        if (file) {	    
            const formData = new FormData();
            formData.append("thumbnail", file);
            return this.http.post(this.ApiUrl+"/nft/uploadFile", formData);
	}

    }

}
