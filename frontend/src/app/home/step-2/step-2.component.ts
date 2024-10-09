import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-step-2',
  templateUrl: './step-2.component.html',
  styleUrls: ['./step-2.component.css']
})
export class Step2Component implements OnInit{

  @Input() loading: boolean = false;
  @Input() loadingMessage!: string;

  @Output() nextStep = new EventEmitter<void>();

  ngOnInit(): void {
  }

}
