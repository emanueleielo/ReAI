import {Component, EventEmitter, Input, Output} from '@angular/core';
import {RequestService} from "../../services/request/request.service";

@Component({
  selector: 'app-step-3',
  templateUrl: './step-3.component.html',
  styleUrls: ['./step-3.component.css']
})
export class Step3Component {
  @Input() downloadFilePath!: string;
  @Output() restart = new EventEmitter();
  loadingDownload: boolean = false;
  downloadComplete: boolean = false;

  constructor(private requestService: RequestService) {
  }

  startDownload() {
    this.loadingDownload = true;
    this.downloadComplete = false;
    this.requestService.downloadFile('download/', this.downloadFilePath).subscribe((response: any) => {
      const { filename, data } = response;
      const blobUrl = URL.createObjectURL(data);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = 'new_project.zip';
      a.click();
      URL.revokeObjectURL(blobUrl); // Libera la memoria
      this.loadingDownload = false;
      this.downloadComplete = true;
    }, (error) => {
      this.loadingDownload = false;
      console.error('error', error);
    });
  }

  restartProcess() {
    this.downloadComplete = false;
    this.restart.emit();
  }

}
