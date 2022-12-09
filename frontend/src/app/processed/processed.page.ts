import { Component, OnInit } from '@angular/core';
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
        res.prefixes.forEach((folderRef) => {
          
          // Find all the items inside the folders
          listAll(folderRef)
            .then((res) => {
              res.items.forEach((itemRef) => {                

                getDownloadURL(itemRef).then((downloadURL) => {

                  // TODO: ADD IF comparison to differentiate between image and json document
                  this.urlList.push(downloadURL);
                  this.imgRefList.push(itemRef.name);

                  console.log(itemRef);
                });
                
              });
              
            }).catch((error) => {
              // Uh-oh, an error occurred!
            });
          
          
        });
        console.log(this.urlList)
      }).catch((error) => {
        // Uh-oh, an error occurred!
      });
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
