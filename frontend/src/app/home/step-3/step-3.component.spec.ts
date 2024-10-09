import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Step3Component } from './step-3.component';

describe('Step3Component', () => {
  let component: Step3Component;
  let fixture: ComponentFixture<Step3Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Step3Component]
    });
    fixture = TestBed.createComponent(Step3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
