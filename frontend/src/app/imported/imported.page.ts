import { Component, OnInit, ViewChild } from '@angular/core';
import { getStorage, ref, listAll, FirebaseStorage, ListOptions, getDownloadURL, deleteObject, uploadBytes, StorageReference } from "firebase/storage";
import { OverlayEventDetail } from '@ionic/core/components';
import { IonModal, ToastController } from '@ionic/angular';
import { HttpClient, HttpHandler } from '@angular/common/http';

@Component({
  selector: 'app-imported',
  templateUrl: './imported.page.html',
  styleUrls: ['./imported.page.scss'],
})
export class ImportedPage implements OnInit {
  storage: FirebaseStorage
  // urlList: string[] = [];
  // imgRefList: string[] = [];
  // urlOfImg: string ="";
  // imageName: string | undefined;
  // pdfSrc: any;
  // imageRef: string | undefined;
  // newImageName: string = ""
  // newFileRef : StorageReference | undefined
  

  references: {[key:number]: {[key: string]: any}} = {}
  referencesArray: string[] = []

  selectedRef : {[key: string]: any} = {}
  newReference : {[key: string]: any} = {}
  
  @ViewChild(IonModal) modal: IonModal | undefined;
  

  constructor(  
      private http: HttpClient,
      private toastController: ToastController
    ) {
    this.storage = getStorage();

   }
  
  ngOnInit() {
    // Create a reference under which you want to list
    const listRef = ref(this.storage, 'unprocessed');
    this.referencesArray = []
    // this.urlList = [];
    // this.imgRefList = [];

    // Find all the prefixes and items.
    listAll(listRef)
      .then((res) => {
        res.items.forEach((itemRef, index) => {    
          this.references[index] = {
            "imageRef": itemRef,
            "imageName": itemRef.name,
            "extension": this.getFileExtension(itemRef.name)
          }      

          getDownloadURL(itemRef).then((downloadURL) => {
            this.references[index]["imageUrl"] = downloadURL
            
            // this.urlList.push(downloadURL);
            // this.imgRefList.push(itemRef.name);
          });
          this.referencesArray.push(index.toString());
        
        });
        
      }).catch((error) => {
        // Uh-oh, an error occurred!
      });
      
  }

  // Refresh page
  handleRefresh(event: any) {
    setTimeout(() => {
      // Any calls to load data go here
      this.ngOnInit()
      event.target.complete();
    }, 2000);
  };

  getFileExtension(fileName: string) {
    // const urlObject = new URL(url);
    // const fileName = urlObject.pathname.split('/').pop();
    // return fileName!.split('.').pop();
    const extension = fileName.split('.')[1]
    if (extension == "pdf"){
      return "pdf"
    }
    else{
      return "image"
    }
  }

  async deleteImage(index: any){
    const storageRef = ref(this.storage, this.references[index]["imageRef"]);
    deleteObject(storageRef).then(() => {
      this.ngOnInit()
    }).catch((error) => {
      // Uh-oh, an error occurred!
    });
  }

  openModal(index: any){
    this.selectedRef = this.references[index]
    

    // this.urlOfImg = this.urlList[index];
    this.newReference = {
      "imageName": this.selectedRef["imageName"],
      "folderName": this.selectedRef["imageName"].split('.')[0]
    }
    // this.newReference["imageName"] = this.references[index]["imageName"];
    // this.newReference["folderName"] = this.references[index]["imageName"].split('.')[0];
    // this.imageRef = this.references[index]["imageName"];
    this.modal?.present();
  }

  cancelModal() {
    this.modal!.dismiss(null, 'cancel');
  }

  confirmModal() {
    this.modal!.dismiss("this.name", 'confirm');
  }
  
  async onWillDismiss(event: Event) {
    const ev = event as CustomEvent<OverlayEventDetail<string>>;
    if (ev.detail.role === 'confirm') {

      this.moveFile()
      // this.processData()
      
    }
  }

  moveFile() {
    const fileRef = this.selectedRef["imageRef"]
    const newFileRef = ref(this.storage, 'processed/' + this.newReference["folderName"] + '/' + fileRef.name);
    this.newReference["fileRef"] = newFileRef

    // Get the download URL for the file
    getDownloadURL(fileRef).then((url) => {
      // Use the download URL to fetch the file data
      this.http.get(url, { responseType: 'blob' }).subscribe(fileData => {

        // upload to new location
        uploadBytes(newFileRef,fileData).then((snapshot) => {
          getDownloadURL(snapshot.ref).then((downloadURL) => {
            console.log('File available at', downloadURL);
            this.newReference["fileUrl"] = downloadURL
            // this.urlOfImg = downloadURL;

            this.sendToast('Successfully moved the file',"success")
            this.processData()
          });
          console.log('File moved to new location.');
          
          
        }).catch(error => {
          console.error('Error moving file:', error);
          this.sendToast('Error while moving the file',"danger")
        });

        

        // delete from old location
        deleteObject(fileRef).then(() => {
          this.ngOnInit()
        }).catch((error) => {
          this.sendToast('Error while moving the file',"danger")
          // Uh-oh, an error occurred!
        });
      });
    }).catch(error => {
      console.error('Error getting file URL:', error);
      this.sendToast('Error while moving the file',"danger")
    });
  }

  // send to the backend the name of the image and its name
  async processData() {

    const hostname = window.location.hostname;
    const url = `http://${hostname}:5000/process/`;

    console.log(this.newReference)

    this.http.post(url,
      {
        img: this.newReference["imageName"],
        folder: this.newReference["folderName"],        
        url: this.newReference["fileUrl"]
      }
    ,{}).subscribe((response) => {
      console.log(response);
      if (response.hasOwnProperty("success")){
        this.sendToast("The file was sent and is being processed","success")
      }
      else{
        this.sendToast("The file could not be sent","danger")
      }
      
    });
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
