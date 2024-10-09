import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-step-2',
  templateUrl: './step-2.component.html',
  styleUrls: ['./step-2.component.css']
})
export class Step2Component implements OnInit{

  loading: boolean = false;
  loadingMessage = 'Loading...';

  @Output() nextStep = new EventEmitter<void>();

  ngOnInit(): void {
    this.startLoading();
  }

  startLoading() {
    this.loading = true;
    this.loadingMessage = 'Loading...';
    setTimeout(() => {
      this.loadingMessage = 'Still loading...';
      setTimeout(() => {
        this.loadingMessage = 'Almost there...';
        setTimeout(() => {
          this.loadingMessage = 'Done!';
          this.loading = false;
          this.nextStep.emit();
        }, 2000);
      }, 2000);
    }, 2000);
  }

}
