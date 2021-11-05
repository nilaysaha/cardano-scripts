import { Component } from '@angular/core';

// import the WindowRef provider
import {WindowRef} from './windowref';


@Component({
    selector: "app-root",
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']    
})

export class AppComponent {
    title = 'NFT Minting App on Cardano';

    constructor(private winRef: WindowRef) {
	var name = 'Angular4'	
	console.log('Window object', winRef.nativeWindow);
  }
}
