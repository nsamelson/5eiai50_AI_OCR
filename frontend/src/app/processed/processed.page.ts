import { Component, OnInit,ViewChild } from '@angular/core';
import { IonModal } from '@ionic/angular';
import { OverlayEventDetail } from '@ionic/core/components';
import { deleteObject, FirebaseStorage, getDownloadURL, getStorage, listAll, ref } from 'firebase/storage';

@Component({
  selector: 'app-processed',
  templateUrl: './processed.page.html',
  styleUrls: ['./processed.page.scss'],
})
export class ProcessedPage implements OnInit {
  storage: FirebaseStorage
  urlList: string[] = [];
  imgRefList: string[] = [];
  urlOfImg: string ="";
  imageName: string | undefined;
  urlDict: {[key: string]: string[]} = {}
  urlOfJson : string =""

  @ViewChild(IonModal) modal: IonModal | undefined;

  constructor() {
    this.storage = getStorage();
   }

  ngOnInit() {
    const listRef = ref(this.storage, 'processed');
    this.urlList = [];
    this.imgRefList = [];

    // Find all the folders.
    listAll(listRef)
      .then((res) => {
        res.prefixes.forEach((folderRef, index) => {
          this.urlDict[index.toString()] = []  

          // Find all the items inside the folders
          listAll(folderRef)
            .then((res) => {
              res.items.forEach((itemRef) => {   
                
                getDownloadURL(itemRef).then((downloadURL) => {
                  
                  
                  if (downloadURL.includes("json")){
                    // console.log(jsonUrl)
                    this.urlDict[index].push(downloadURL)
                  }
                  else{
                    this.urlDict[index].unshift(downloadURL)
                    this.urlList.push(downloadURL);
                    this.imgRefList.push(itemRef.name);
                  }
                  

                });
                
                
              });
              
              
            }).catch((error) => {
              // Uh-oh, an error occurred!
            });

            // this.urlDict[index] = [imageUrl,jsonUrl]
          
          
        });
        console.log(this.urlList)
        console.log(this.urlDict)
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
    // const storageRef = ref(this.storage, "processed/"+this.imgRefList[index]);
    // deleteObject(storageRef).then(() => {
    //   this.ngOnInit()
    // }).catch((error) => {
    //   // Uh-oh, an error occurred!
    // });
  }


  openModal(index: any){
    this.urlOfImg = this.urlList[index];
    this.urlOfJson = this.urlDict[index][1]
    //TODO: Show the content of the JSON file

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
      // this.processData()
    }
  }

  // async deleteImage(index: any){
  //   const storageRef = ref(this.storage, "processed/"+this.imgRefList[index]);
  //   deleteObject(storageRef).then(() => {
  //     this.ngOnInit()
  //   }).catch((error) => {
  //     // Uh-oh, an error occurred!
  //   });
  // }

}
