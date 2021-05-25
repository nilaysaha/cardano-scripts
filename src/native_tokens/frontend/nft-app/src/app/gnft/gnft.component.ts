import { Component, OnInit } from '@angular/core';
import { RecaptchaErrorParameters } from "ng-recaptcha";
import { NFT } from './gnft';
import { NftService } from './gnft.service';

@Component({
  selector: 'app-gnft',
  templateUrl: './gnft.component.html',
  styleUrls: ['./gnft.component.css']
})


export class GnftComponent implements OnInit {

    model = new NFT('NFTS',10, 100, "safety, loyalty", 'addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j', '/ipfs/testing');
    buttonDisabled: boolean;
    submitted: boolean = false;
    
    constructor(private NftService: NftService) {}
    
    ngOnInit(): void {
	this.buttonDisabled = true;
    }

    onSubmit(): void {
	console.log(`Pressed submit for submitting`)
	console.log(this.model)
	this.submitted = true;
	this.NftService.createNft(this.model)
    }
    
    // TODO: Remove this when we're done
    get diagnostic() { return JSON.stringify(this.model); }

    public resolved(captchaResponse: string): void {
	console.log(`Resolved captcha with response: ${captchaResponse}`);
	if (captchaResponse != null){
	    this.buttonDisabled = false;
	}
	else{
	    this.buttonDisabled = true;
	}
    }

    public onError(errorDetails: RecaptchaErrorParameters): void {
	console.log(`reCAPTCHA error encountered; details:`, errorDetails);
	this.buttonDisabled = true;
    }


}
