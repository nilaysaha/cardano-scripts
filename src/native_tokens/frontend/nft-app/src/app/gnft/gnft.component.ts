import { Component, OnInit } from '@angular/core';
import { RecaptchaErrorParameters } from "ng-recaptcha";
import { NFT } from './gnft';
import { NFTPay } from './gnftPay';
import { NftService } from './gnft.service';

import { onAuthUIStateChange, CognitoUserInterface, AuthState } from '@aws-amplify/ui-components';

@Component({
  selector: 'app-gnft',
  templateUrl: './gnft.component.html',
  styleUrls: ['./gnft.component.css']
})



export class GnftComponent implements OnInit {

    model: NFT = new NFT("NTFS", 10, "lasting value", 'addr_test1vzezxpug0fuehlk4edj0chk4a7ehvkc704z7sr4mggc68uqccxdmq', "/ipfs/testing" );    
    payModel: NFTPay = new NFTPay("fdf66851-748a-4f9a-ac20-e0e13791c27a(Dummy)",100, "ADA", "addr_test1vpyk92350x8gajyefdr44lk5jmjn9f8y4udfxw34pka5pvgjqxw4j(Dummy)");
    
    buttonDisabled: boolean;
    submitted: boolean = false;
    reqSucceeded: boolean = false;
    fileName: string;
    msg: string;
    url: any = "https://plchldr.co/i/1000x500?fc=111111&&text=Image placeholder"
    ipfsLink: string;
    
    constructor(private NftService: NftService) {}
    
    ngOnInit(): void {
    }
    
    _checkFile(event){
	var mimeType = event.target.files[0].type;
	
	if(!event.target.files[0] || event.target.files[0].length == 0) {
	    this.msg = 'You must select an image';
	    return;
	}
	
	if (mimeType.match(/image\/*/) == null) {
	    this.msg = "Only images are supported";
	    return;
	}	
    }
    
    onFileSelected(event):void {
	const file:File = event.target.files[0];
	
	if (file) {
	    this.fileName = file.name;
	    console.log(`value of reqSucceeded:${this.reqSucceeded}`)

	    //This will later be extended for different kind of files to be uploaded
	    this._checkFile(event)

	    //this ensures we show the image
	    var reader = new FileReader();
	    reader.readAsDataURL(event.target.files[0]);
	    reader.onload = (_event) => {
		this.msg = "";
		this.url = reader.result; 
	    }

	    this.NftService.uploadFile(file)
		.subscribe(val => {
		    console.log("POST call successful to backend for uploading file")
		    console.log(val)
		})
	}
    }


    onSubmit(): void {
	console.log(`Pressed submit for submitting`)
	console.log(this.model)
	this.submitted = true;
	this.NftService.createNft(this.model)
	    .subscribe(
		val => {
		    console.log("POST call successful value returned in body", 	val);
		    this.reqSucceeded = true;
		    this.payModel.assetID = val.uuid;
		    this.payModel.currency = val.currency;
		    this.payModel.payAddr = val.payment_addr;
		    this.payModel.mintingCost = val.mintingCost;
		},
		response => {
		    console.log("POST call in error", response);
		},
		() => {
		    console.log("The POST observable is now completed.");
		}
	    );	

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

    public onLoad(): void {
	console.log("recaptcha is loaded")
    }

}
