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
  uploadedImg: String | undefined;
  imageName: string | undefined;
  pdfSrc: any;

  constructor(private toastController: ToastController) { 
    // this.app = initializeApp(environment.firebaseConfig);
  }

  selectImage(event: any){
    this.selectedFile = event.target.files[0];
    console.log(this.selectedFile);   
    this.imageName = this.selectedFile!.name

    // Check if the file is an image or a pdf
    if (this.selectedFile!.type.startsWith('image/')) {
      this.clearPreview("pdfSrc");
      this.previewImage(this.selectedFile!);
    } 
    else if (this.selectedFile!.type === 'application/pdf') {      
      this.clearPreview("uploadedImg");     
      this.previewPDF(this.selectedFile!);
    }
  };

  // Function to preview the image
  previewImage(image: File) {
    // Create a FileReader object
    const reader = new FileReader();

    // Add an event listener to execute when the file has been read
    reader.addEventListener('load', () => {
      // Get the preview element
      const preview = document.getElementById('uploadedImg') as HTMLImageElement;

      // Set the src attribute of the preview element to the data URL of the image
      preview.src = reader.result as string;      
    });

    // Read the image file as a data URL
    reader.readAsDataURL(image);
  }

  // Function to preview the PDF
  async previewPDF(pdf: File) {

    if (typeof (FileReader) !== 'undefined') {
      let reader = new FileReader();
  
      reader.onload = (e: any) => {
        this.pdfSrc = e.target.result;
      };

      // Read the image file as a data URL
      reader.readAsArrayBuffer(pdf);
    }
  }

  // Function to clear the image preview
  clearPreview(src: string) {
    // Get the preview element
    try {
      if (src == "pdfSrc"){
        this.pdfSrc = null
      }
      else{
        const preview = document.getElementById(src) as HTMLImageElement;
        preview.src = '';
      }
    }
    catch{
      console.log("no src")
    }   
  }

  // Create a form data object using the FormData API
  async submitForm(){

    // Add the file that was just added to the form data
    if(this.selectedFile != null){
      // formData.append("photo", this.selectedFile!, this.selectedFile!.name);
      if (this.selectedFile.type.startsWith('image/') || this.selectedFile.type === 'application/pdf'){
        this.uploadImage(this.selectedFile)
      }
      else{
        this.sendToast('Please choose a file in the PNG or PDF format',"warning")
      }
    }
    else{
      this.sendToast('Please choose a file in the PNG or PDF format',"warning")
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

  async uploadImage(cameraFile: File) {

    const storage = getStorage();
    const storageRef = ref(storage, "unprocessed/"+this.imageName);
    
    uploadBytes(storageRef, cameraFile).then((snapshot) => {
      console.log('Uploaded a blob or file!');
      this.sendToast('The file has been uploaded!',"success")

      getDownloadURL(snapshot.ref).then((downloadURL) => {
        console.log('File available at', downloadURL);
        this.uploadedImg = downloadURL;
      });
  
    });


	}

  


}
