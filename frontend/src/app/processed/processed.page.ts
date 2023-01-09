import { HttpClient } from '@angular/common/http';
import { Component, OnInit,ViewChild } from '@angular/core';
import { IonModal, ToastController } from '@ionic/angular';
import { OverlayEventDetail } from '@ionic/core/components';
import { deleteObject, FirebaseStorage, getDownloadURL, getStorage, listAll, ref } from 'firebase/storage';
import { child, Database, getDatabase, ref as dbRef, set, get, push, update  } from "firebase/database";



@Component({
  selector: 'app-processed',
  templateUrl: './processed.page.html',
  styleUrls: ['./processed.page.scss'],
})
export class ProcessedPage implements OnInit {
  storage: FirebaseStorage
  database: Database
  urlList: string[] = [];
  imgRefList: string[] = [];
  urlOfImg: string ="";
  imageName: string | undefined;
  urlDict: {[key: string]: string[]} = {}
  urlOfJson : string =""
  jsonContent = {"nothing": "to show"}
  jsonString = "Nothing to show"

  @ViewChild(IonModal) modal: IonModal | undefined;
  

  constructor(private http: HttpClient,private toastController: ToastController) {
    this.storage = getStorage();
    this.database = getDatabase();
    
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

  // update content of the JSON
  writeData(path: string, updates: { [key: string]: any }) {
    update(child(dbRef(this.database), `processed/${path}`),updates )
  }

  // read the content of the JSON and update JSON content then stringifies it
  readData(docRef: string){
    get(child(dbRef(this.database), `processed/${docRef}`)).then((snapshot) => {
      if (snapshot.exists()) {
        console.log(snapshot.val());
        this.jsonContent = snapshot.val()        
      } else {
        this.jsonContent = {"nothing": "to show"}
      }
      this.jsonString = JSON.stringify(
        this.jsonContent, 
        (key, value) => {
          if (typeof value === 'string') {
            return value.replace(/,/g, '\\n');
          }
          return value;
        }, 2);
      console.log(this.jsonString)
    }).catch((error) => {
      console.error(error);
    });
  }


  openModal(index: any){
    this.urlOfImg = this.urlList[index];
    this.urlOfJson = this.urlDict[index][1]
    this.imageName = this.imgRefList[index];

    // get(child(dbRef(this.database),"processed/"))

    this.readData(this.imageName.split('.')[0])
    console.log(this.imageName)


    // this.imageRef = this.imgRefList[index];
    this.modal?.present();
  }

  cancelModal() {
    this.modal!.dismiss(null, 'cancel');
  }

  confirmModal() {    
    try{
      var newJson = JSON.parse(this.jsonString)
      this.writeData(this.imageName!.split('.')[0],newJson)
      this.sendToast('The data was succesfully changed and updated!',"success")
      this.modal!.dismiss("this.name", 'confirm');
    }catch{
      this.sendToast('There is an error in the format of the JSON',"warning")
    } 
    
  }
  
  onWillDismiss(event: Event) {
    const ev = event as CustomEvent<OverlayEventDetail<string>>;
    if (ev.detail.role === 'confirm') {
      // this.processData()
    }
  }

   // Send Toast with error or success of upload
   async sendToast(msg:string, success: string){
    const toast = await this.toastController.create({
      message: msg,
      duration: 1500,
      position: 'bottom',
      color: success
    });

    await toast.present();
      
  }

}
