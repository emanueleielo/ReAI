import {Component, EventEmitter, Output} from '@angular/core';

@Component({
  selector: 'app-step-3',
  templateUrl: './step-3.component.html',
  styleUrls: ['./step-3.component.css']
})
export class Step3Component {

  loadingDownload: boolean = false;
  downloadComplete: boolean = false;
  @Output() restart = new EventEmitter();


  startDownload() {
    this.loadingDownload = true;
    setTimeout(() => {
      this.loadingDownload = false;
      this.downloadComplete = true;
    }, 3000);
  }

  restartProcess() {
    this.downloadComplete = false;
    this.restart.emit();
  }

}
