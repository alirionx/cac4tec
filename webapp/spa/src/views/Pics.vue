<template>
  <div class="Pics">
    <div class="pageHl">Mash: {{mashObj.name}}</div>
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

    <table class="stdTbl">
      <thead>
        <tr>
          <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign:col.align}">{{col.hl}}</th>
          <th>Thumb</th>
          <th>Act</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in pics" :key="idx">
          <td v-for="(col, idx) in defi" :key="idx" :style="{textAlign:col.align}">{{row[col.col]}}</td>
          <td>
            <img :src="row.thumbpath" @mouseover="toggle_pic_prev(idx)" @mouseout="toggle_pic_prev(idx)" />
          </td>
          <td>
            <button v-on:click="call_remove_pic(idx)">del</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="picPrevBox" v-if="picPrev!=null">
      <img :src="picPrev" />
    </div>

    <ConfirmBox v-if="confirmMsg!=null"
      v-bind:msg = confirmMsg
      v-bind:callback = reset_confirm
      v-bind:fw = confirmFw
    />

    <Loader v-if="loader" />

  </div>
</template>

<script>
import axios from 'axios'
import Loader from '@/components/Loader.vue'
import ConfirmBox from '../components/ConfirmBox.vue'

export default {
  name: 'Pics',
  components: {
    Loader,
    ConfirmBox
  },
  data(){
    return{
      mash: this.$route.params.id,
      mashObj: {name: "" },
      admin: false,
      loader: false,
      confirmMsg: null,
      confirmFw: ()=>{},
      pics: [],
      picPrev: null,
      defi: [
        {
          col: "id",
          hl: "DBId",
          align: "center"
        },
        {
          col: "added",
          hl: "Added",
          align: "center"
        },
        {
          col: "won",
          hl: "Won",
          align: "center"
        },
        {
          col: "loss",
          hl: "Loss",
          align: "center"
        },
        {
          col: "rate",
          hl: "Rating",
          align: "center"
        }
      ],
      uploadList: [],
    }
  },
  methods:{
    call_pics(){
      this.loader = true;
      axios.get("/api/pics/"+this.mash).then(response => { 
        console.log(response.data);
        this.pics = response.data.data;
        this.mashObj = response.data.mash;
        this.admin = response.data.admin;
        this.loader = false;
      })
      .catch(error => {
        console.log(error);
        this.loader = false;
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
        this.call_pics();
      })
      .catch(error => {
        console.log('Upload failed.');
        this.loader = false;
        this.reset_upload();
      });
    },
    reset_upload(){
      this.uploadList = [];
    },

    call_remove_pic(idx){
      this.confirmMsg = "Do you really want do delete image "+this.pics[idx].id+"?";
      var fwFunc = this.remove_pic;
      this.confirmFw = function(){ fwFunc(idx) }
    },

    remove_pic(idx){
      let id = this.pics[idx].id;
      axios.delete("/api/pic/"+id ).then(response => { 
        console.log(response.data);
        this.pics.splice(idx, 1); 
      })
      .catch(error => {
        console.log(error);
      });
    },

    toggle_pic_prev(idx){
      let picId = this.pics[idx].id;
      let picMime = this.pics[idx].mime;
      let picPrev = this.pics[idx].imagepath
      if(picPrev == this.picPrev){
        this.picPrev = null;
      } 
      else{
        this.picPrev = picPrev;
      } 
    },

    reset_confirm(){
      this.confirmMsg = null;
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

.picPrevBox{
  position: fixed;
  bottom:10px;
  left:10px;
  padding: 6px;
  width:35%;
  min-width: 400px;
  min-height:40px;
  text-align:left;
  padding:10px;
  box-shadow: 1px 1px #fff;
  background-color: #333;
  *opacity: 0.8;
  color:#fff;
  cursor: pointer;
  text-align: center;
}
.picPrevBox img{
  width: 100%;
  box-shadow: 1px 1px #fff;
}


</style>
