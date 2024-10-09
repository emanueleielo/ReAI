import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  step = 1;

  constructor() { }

  nextStep() {
    this.step++;
  }

  restart() {
    this.step = 1;
  }

}
