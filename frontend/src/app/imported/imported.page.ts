import { Component, OnInit } from '@angular/core';
import { getStorage, ref, listAll, FirebaseStorage, ListOptions, getDownloadURL, deleteObject } from "firebase/storage";

@Component({
  selector: 'app-imported',
  templateUrl: './imported.page.html',
  styleUrls: ['./imported.page.scss'],
})
export class ImportedPage implements OnInit {
  storage: FirebaseStorage
  urlList: string[] = [];
  imgRefList: string[] = [];

  constructor() {
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
        console.log(this.urlList)
      }).catch((error) => {
        // Uh-oh, an error occurred!
      });
  }

  async deleteImage(index: any){
    const storageRef = ref(this.storage, "unprocessed/"+this.imgRefList[index]);
    deleteObject(storageRef).then(() => {
      this.ngOnInit()
    }).catch((error) => {
      // Uh-oh, an error occurred!
    });
  }

  

}
