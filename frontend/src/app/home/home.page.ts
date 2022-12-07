import { Component } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { getDownloadURL, ref, getStorage, uploadString,uploadBytes } from 'firebase/storage';




@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  selectedFile: File | undefined;
  app: any;
  uploadedImg: String | undefined;

  constructor(private toastController: ToastController) { 
    // this.app = initializeApp(environment.firebaseConfig);
  }

  selectImage(event: any){
    this.selectedFile = event.target.files[0];
    console.log(this.selectedFile);   
    
  };

  async submitForm(){
    // Create a form data object using the FormData API
    let formData = new FormData();

    // Add the file that was just added to the form data
    if(this.selectedFile != null){
      formData.append("photo", this.selectedFile!, this.selectedFile!.name);
      console.log(formData);

      // this.http.post('http')
      this.uploadImage(this.selectedFile)
    }
    else{
      const toast = await this.toastController.create({
        message: 'Please choose an file in the PNG or PDF format',
        duration: 1500,
        position: 'bottom'
      });
  
      await toast.present();
    }
    
  }

  async uploadImage(cameraFile: File) {

    const storage = getStorage();
    const storageRef = ref(storage, "unprocessed/"+cameraFile.name);
    
    uploadBytes(storageRef, cameraFile).then((snapshot) => {
      console.log('Uploaded a blob or file!');

      getDownloadURL(snapshot.ref).then((downloadURL) => {
        console.log('File available at', downloadURL);
        this.uploadedImg = downloadURL;
      });
  
    });


	}

  


}
