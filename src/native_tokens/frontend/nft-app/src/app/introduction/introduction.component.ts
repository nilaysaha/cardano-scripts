import { Component, OnInit, Inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';


@Component({
  selector: 'app-introduction',
  templateUrl: './introduction.component.html',
  styleUrls: ['./introduction.component.css']
})
export class IntroductionComponent implements OnInit {

    buttonType: string

    
    constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService) {}
    
    ngOnInit(): void {}

    action():any {
	console.log("Now doing action")
	this.auth.isAuthenticated$.subscribe(data => {
	    if (data){
		console.log("Logging out the user")
		this.auth.logout({ returnTo: window.top.location.origin })
		console.log(`status of logout:${this.auth.isAuthenticated$}`)		
	    }
	    else
	    {
		console.log("Now trying to login the user")
		this.auth.loginWithRedirect()
	    }
	})
    }    

}
