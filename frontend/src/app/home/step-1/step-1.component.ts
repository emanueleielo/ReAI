import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Configuration} from "../../models/configuration/configuration";

@Component({
  selector: 'app-step-1',
  templateUrl: './step-1.component.html',
  styleUrls: ['./step-1.component.css']
})
export class Step1Component {
  @Input() loading = false;
  @Output() startRefactoring = new EventEmitter<Configuration>();
  configuration: Configuration = {} as Configuration;

  start() {
    if (this.configuration.tech_language && this.configuration.tech_framework && this.configuration.zip_file) {
      this.startRefactoring.emit(this.configuration)
    }
  }
}
