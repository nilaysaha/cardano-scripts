import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Import the module from the SDK
import { AuthModule } from '@auth0/auth0-angular';


import {MatFormFieldModule} from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import {MatDividerModule} from '@angular/material/divider';

import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatIconModule} from '@angular/material/icon';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import {MatStepperModule} from '@angular/material/stepper';


import { RecaptchaModule } from "ng-recaptcha";
import { GnftComponent } from './gnft/gnft.component'; 
import { NftService } from './gnft/gnft.service';
import { IntroductionComponent } from './introduction/introduction.component';

import { RouterModule } from '@angular/router';
import { FaqComponent } from './faq/faq.component';
import { AuthComponent } from './auth/auth.component';
import { NavbarComponent } from './navbar/navbar.component';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';
import { FooterComponent } from './footer/footer.component';

// Import the authentication guard
import { AuthGuard } from '@auth0/auth0-angular';

@NgModule({
    declarations: [
	AppComponent,
	GnftComponent,
	IntroductionComponent,
	FaqComponent,
	AuthComponent,
	NavbarComponent,
	PagenotfoundComponent,
	FooterComponent,
    ],
    imports: [
	BrowserModule,
	BrowserAnimationsModule,
	MatFormFieldModule,
	MatInputModule,
	MatDividerModule,
	MatButtonModule,
	MatIconModule,
	RecaptchaModule,
	FormsModule,
	HttpClientModule,
	MatStepperModule,
	MatGridListModule,
	AuthModule.forRoot({
	    domain: 'nft-cardano.eu.auth0.com',
	    clientId: 'h4YsBPze0ERS2X9uQmpS67XI22gzVuLM'
	}),
	RouterModule.forRoot([
      	    {path: '', redirectTo: 'home', pathMatch: 'full'},
	    {path: 'home', component: IntroductionComponent},
      	    {path: 'nft-issue', component: GnftComponent, canActivate: []},
	    {path: 'faq', component: FaqComponent},
	    {path: '**', component: PagenotfoundComponent}
	]),
    ],
    exports: [RouterModule],
    providers: [],
    bootstrap: [AppComponent]
})

export class AppModule { }
