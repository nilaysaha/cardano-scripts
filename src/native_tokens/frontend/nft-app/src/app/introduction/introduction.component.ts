import { Component, OnInit, Inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';


@Component({
  selector: 'app-introduction',
  templateUrl: './introduction.component.html',
  styleUrls: ['./introduction.component.css']
})
export class IntroductionComponent implements OnInit {

    constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService) { }
    
    ngOnInit(): void {
    }

    isLoggedIn(){
	
    }

}
