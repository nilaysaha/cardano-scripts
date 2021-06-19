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

@NgModule({
    declarations: [
	AppComponent,
	GnftComponent,
	IntroductionComponent,
	FaqComponent,
 AuthComponent,
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
	// Import the module into the application, with configuration
	AuthModule.forRoot({
	    domain: 'nft-cardano.eu.auth0.com',
	    clientId: 'h4YsBPze0ERS2X9uQmpS67XI22gzVuLM'
	}),
	RouterModule.forRoot([
      	    {path: '', component: IntroductionComponent},
      	    {path: 'nft-issue', component: GnftComponent},
	    {path: 'faq', component: FaqComponent},
	    {path: 'login', component: AuthComponent},
	]),
    ],
    exports: [RouterModule],
    providers: [],
    bootstrap: [AppComponent]
})

export class AppModule { }
