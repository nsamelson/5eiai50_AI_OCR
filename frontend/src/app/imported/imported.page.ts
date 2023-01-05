import { Component, OnInit, ViewChild } from '@angular/core';
import { getStorage, ref, listAll, FirebaseStorage, ListOptions, getDownloadURL, deleteObject } from "firebase/storage";
import { OverlayEventDetail } from '@ionic/core/components';
import { IonModal } from '@ionic/angular';
import { HttpClient, HttpHandler } from '@angular/common/http';

@Component({
  selector: 'app-imported',
  templateUrl: './imported.page.html',
  styleUrls: ['./imported.page.scss'],
})
export class ImportedPage implements OnInit {
  storage: FirebaseStorage
  urlList: string[] = [];
  imgRefList: string[] = [];
  urlOfImg: string ="";
  imageName: string | undefined;
  pdfSrc: any;
  // imageRef: string | undefined;
  
  @ViewChild(IonModal) modal: IonModal | undefined;
  

  constructor(  
      private http: HttpClient
    ) {
    this.storage = getStorage();

   }
  
  ngOnInit() {
    // Create a reference under which you want to list
    const listRef = ref(this.storage, 'unprocessed');
    this.urlList = [];
    this.imgRefList = [];

    // Find all the prefixes and items.
    listAll(listRef)
      .then((res) => {
        res.items.forEach((itemRef) => {
          

          getDownloadURL(itemRef).then((downloadURL) => {
            this.urlList.push(downloadURL);
            this.imgRefList.push(itemRef.name);
          });
          
        });
        // console.log(this.urlList)
      }).catch((error) => {
        // Uh-oh, an error occurred!
      });
  }

  getFileExtension(url: string) {
    const urlObject = new URL(url);
    const fileName = urlObject.pathname.split('/').pop();
    return fileName!.split('.').pop();
  }

  async deleteImage(index: any){
    const storageRef = ref(this.storage, "unprocessed/"+this.imgRefList[index]);
    deleteObject(storageRef).then(() => {
      this.ngOnInit()
    }).catch((error) => {
      // Uh-oh, an error occurred!
    });
  }

  openModal(index: any){
    this.urlOfImg = this.urlList[index];

    // const fileExtension = this.getFileExtension(this.urlOfImg)
    // if (fileExtension == "pdf"){
      
    // }

    this.imageName = this.imgRefList[index];
    // this.imageRef = this.imgRefList[index];
    this.modal?.present();
  }

  cancelModal() {
    this.modal!.dismiss(null, 'cancel');
  }

  confirmModal() {
    this.modal!.dismiss("this.name", 'confirm');
  }
  
  onWillDismiss(event: Event) {
    const ev = event as CustomEvent<OverlayEventDetail<string>>;
    if (ev.detail.role === 'confirm') {
      this.processData()
    }
  }

  // API CALL

  async processData() {

    const hostname = window.location.hostname;
    const url = `http://${hostname}:5000/process/`;

    this.http.post(url,{
        img: this.imageName,
        url: this.urlOfImg
    },{}).subscribe((response) => {
      console.log(response);
    });
  }

}
