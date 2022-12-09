import { Component } from '@angular/core';
import { MenuController } from '@ionic/angular';
import { Router } from '@angular/router';

import {Injectable} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
@Injectable()
export class AppComponent {
  constructor(private menuCtrl: MenuController, private router: Router) {
    
  }

  

  openMenu() {
    this.menuCtrl.open();
  }

  closeMenu() {
    this.menuCtrl.close();
  }
  
  goToHomePage() {
    this.router.navigate(['/']);
  }


}
