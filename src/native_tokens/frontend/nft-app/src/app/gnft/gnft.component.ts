import { Component, OnInit } from '@angular/core';
import { RecaptchaErrorParameters } from "ng-recaptcha";
import { NFT } from './gnft';

@Component({
  selector: 'app-gnft',
  templateUrl: './gnft.component.html',
  styleUrls: ['./gnft.component.css']
})


export class GnftComponent implements OnInit {

    apiUrl="https://nft.oef.io/api"
    model = new NFT(18, 'NFTS', "safety, loyalty", 'addr_test1vrsk2nj9dnxuawsf2x9j7e4salp2qw4zjrz98kadt5er69gxh0376');
    buttonDisabled: boolean;
    
    constructor() {
    }
    
    ngOnInit(): void {
	this.buttonDisabled = true;
    }
    
    // TODO: Remove this when we're done
    get diagnostic() { return JSON.stringify(this.model); }

    public resolved(captchaResponse: string): void {
	console.log(`Resolved captcha with response: ${captchaResponse}`);
	this.buttonDisabled = false;
    }

    public onError(errorDetails: RecaptchaErrorParameters): void {
	console.log(`reCAPTCHA error encountered; details:`, errorDetails);
    }


}
