import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GnftComponent } from './gnft.component';

describe('GnftComponent', () => {
  let component: GnftComponent;
  let fixture: ComponentFixture<GnftComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GnftComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GnftComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
