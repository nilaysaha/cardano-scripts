import {Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
 
const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};
 
@Injectable()
export class ApiService {
 
    constructor(private http:HttpClient) {}

    createNft(nftModel) {
        let body = JSON.stringify(nftModel);
        return this.http.post('/nft', body, httpOptions);
    }

   
}
