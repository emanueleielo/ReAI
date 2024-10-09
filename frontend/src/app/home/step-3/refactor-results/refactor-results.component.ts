import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-refactor-results',
  templateUrl: './refactor-results.component.html',
  styleUrls: ['./refactor-results.component.css']
})
export class RefactorResultsComponent {

  @Input() loadingDownload: boolean = false;

}
