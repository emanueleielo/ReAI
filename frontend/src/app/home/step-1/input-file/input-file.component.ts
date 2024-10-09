import {Component, EventEmitter, Output} from '@angular/core';

@Component({
  selector: 'app-input-file',
  templateUrl: './input-file.component.html',
  styleUrls: ['./input-file.component.css']
})
export class InputFileComponent {

  @Output() emitFile = new EventEmitter<File[]>();
  selectedFile: File[] = [];

  openFileInput(fileInput: HTMLInputElement) {
    fileInput.click();
  }

  handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      Array.from(input.files).forEach(file => {
        this.selectedFile.push(file);
        this.emitFile.emit(this.selectedFile);
      });
    }
  }

  formatFileSize(size: number): string {
    const units = ['B', 'KB', 'MB', 'GB'];
    let index = 0;

    while (size >= 1024 && index < units.length - 1) {
      size /= 1024;
      index++;
    }

    return `${size.toFixed(2)} ${units[index]}`;
  }

  removeFile(index: number) {
    this.selectedFile.splice(index, 1);
    this.emitFile.emit(this.selectedFile);
  }

}
