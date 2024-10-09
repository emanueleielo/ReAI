import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Step2Component } from './step-2.component';

describe('Step2Component', () => {
  let component: Step2Component;
  let fixture: ComponentFixture<Step2Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Step2Component]
    });
    fixture = TestBed.createComponent(Step2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
