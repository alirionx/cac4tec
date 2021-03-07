<template>
  <div class="Pics">
    <div class="picUpload" v-if="admin">
      <input type="file" id="imageSelectIpt" v-on:change="apply_file_select" multiple accept="image/png, image/jpeg, image/jpg" />
      <div class="uploadHl">Images to upload</div>
      <div class="uploadList" v-on:click="call_file_select">
        <div v-if="uploadList.length==0">click to select...</div>
        <div v-for="(file, idx) in uploadList" :key="idx"> - {{file}}</div>
      </div>

      <div class="btnFrame" v-if="uploadList.length>0">
        <button v-on:click="submit_upload">upload</button>
        <button v-on:click="reset_upload">cancel</button>
      </div>
    </div>

    <pre>{{pics}}</pre>

    <Loader v-if="loader" />
  </div>
</template>

<script>
import axios from 'axios'
import Loader from '@/components/Loader.vue'

export default {
  name: 'Pics',
  components: {
    Loader
  },
  data(){
    return{
      mash: this.$route.params.id,
      admin: false,
      loader: false,
      pics: [],
      uploadList: [],
    }
  },
  methods:{
    call_pics(){
      axios.get("/api/pics/"+this.mash).then(response => { 
        console.log(response.data);
        this.pics = response.data.data;
        this.admin = response.data.admin;
      })
      .catch(error => {
        console.log(error);
      });
    },
    
    call_file_select(){
      let domEl = document.getElementById("imageSelectIpt");
      domEl.click();
    },
    apply_file_select(){
      let domEl = document.getElementById("imageSelectIpt");
      //console.log(domEl.files);
      this.uploadList = [];
      for(let prop in domEl.files){
        let file = domEl.files[prop];
        if(file.type != undefined){  
          if(file.type.startsWith("image")){
            this.uploadList.push(file.name);
          }
        }
      }
    },

    submit_upload(){
      this.loader = true;
      let domEl = document.getElementById("imageSelectIpt");
      let formData = new FormData();

      for( var i = 0; i < domEl.files.length; i++ ){
        let file = domEl.files[i];
        formData.append('file', file);
      }

      const headers= {'Content-Type': 'multipart/form-data'}
      axios.post( '/api/pics/'+this.mash, formData, headers).then(response => { 
        console.log('Upload successful.');
        this.loader = false;
        this.reset_upload();
      })
      .catch(error => {
        console.log('Upload failed.');
        this.loader = false;
        this.reset_upload();
      });
    },
    reset_upload(){
      this.uploadList = [];
    }

  },
  
  created: function(){
    this.call_pics();
  },
  mounted: function(){
    
    
  },
}
</script>


<style scoped>
.picUpload{
  margin: 4px auto auto auto;

}
.picUpload input[type=file]{
  display:none;
}
.picUpload .uploadHl{
  padding:8px;
  font-size: 18px;
  font-weight: bold;
}
.picUpload .uploadList{
  display: table;
  margin:auto auto auto;
  min-width:400px;
  min-height:40px;
  text-align:left;
  padding:10px;
  *border: 1.5px solid #444;
  box-shadow: 1px 1px #fff;
  background-color: #444;
  color:#fff;
  cursor: pointer;
}
.picUpload .uploadList div{
  padding:3px;
}

.picUpload .btnFrame{
  text-align: center;
  padding:10px;
}
.picUpload .btnFrame button{
  min-width:90px;
  background-color: #444;
  color:#fff;
  text-align:center;
  font-size:16px;
  padding:4px;
  margin: auto 8px auto 8px;
  *border-radius: 8px;
  border: none;
  box-shadow: 1px 1px #fff;
  cursor:pointer;
  font-family: 'Courier New', Courier, monospace;
}
.picUpload .btnFrame button:hover{
  background-color: #333;
}

</style>
