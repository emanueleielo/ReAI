import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Step1Component } from './step-1.component';

describe('Step1Component', () => {
  let component: Step1Component;
  let fixture: ComponentFixture<Step1Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Step1Component]
    });
    fixture = TestBed.createComponent(Step1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
