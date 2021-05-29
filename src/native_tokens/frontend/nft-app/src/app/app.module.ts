import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {MatFormFieldModule} from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import {MatDividerModule} from '@angular/material/divider';

import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatGridListModule} from '@angular/material/grid-list';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import {MatStepperModule} from '@angular/material/stepper';

import { RecaptchaModule } from "ng-recaptcha";
import { GnftComponent } from './gnft/gnft.component'; 
import { NftService } from './gnft/gnft.service';


@NgModule({
  declarations: [
      AppComponent,
      GnftComponent
  ],
  imports: [
      BrowserModule,
      BrowserAnimationsModule,
      MatFormFieldModule,
      MatInputModule,
      MatDividerModule,
      MatButtonModule,
      RecaptchaModule,
      FormsModule,
      HttpClientModule,
      MatStepperModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule { }
