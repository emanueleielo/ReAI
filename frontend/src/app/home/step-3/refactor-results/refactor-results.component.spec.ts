import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RefactorResultsComponent } from './refactor-results.component';

describe('RefactorResultsComponent', () => {
  let component: RefactorResultsComponent;
  let fixture: ComponentFixture<RefactorResultsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RefactorResultsComponent]
    });
    fixture = TestBed.createComponent(RefactorResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
