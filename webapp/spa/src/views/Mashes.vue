<template>
  <div class="Mashes">
    
    <div class="pageHl" v-if="mashes.length==0">No mashes available</div>

    <div class="selectFrame">
      <select v-on:change="call_pics" v-model="selected_mash" v-if="mashes.length>0">
        <option v-if="selected_mash==null" value="null">Please select a mash</option>
        <option v-for="(mash, idx) in mashes" :key="idx" :value="idx">{{mash.name}}</option>
      </select>
      <button class="sideBtn" v-if="selected_mash!=null" v-on:click="call_rating">show rating</button>
      <div class="mashDesc" v-if="selected_mash!=null">{{selected_mash_desc}}</div>
    </div>  

    <table class="mashFrame" v-if="selected_mash!=null"><tr>
      <td v-for="(pic, idx) in data" :key="idx">
        <img :src="pic.imagepath" v-on:click="rate_pic(idx)" />
      </td>
    </tr></table>

  </div>
</template>

<script>
import axios from 'axios'
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Mashes',
  components: {
    //HelloWorld
  },
  data(){
    return{
      mashes: [],
      data: [],
      selected_mash: null,
      selected_mash_desc: ""
    }
  },
  methods:{
    call_mashes(){
      axios.get("/api/mashes").then(response => { 
        console.log(response.data);
        this.mashes = response.data.data;
      })
      .catch(error => {
        console.log(error);
      });
    },
    
    call_pics(){
      this.selected_mash_desc = this.mashes[this.selected_mash].description;
    
      axios.get("/api/rate/"+this.mashes[this.selected_mash].id).then(response => { 
        console.log(response.data);
        this.data = response.data.data;
      })
      .catch(error => {
        console.log(error.response);
      });
    },

    call_rating(){
      location.hash = "/pics/"+this.mashes[this.selected_mash].id
    },

    rate_pic(idx){
      let wonPicId = this.data[idx].id;
      let tmpAry = this.data.slice();
      tmpAry.splice(idx, 1);
      let lossPicId = tmpAry[0].id;

      //console.log(wonPicId);
      //console.log(lossPicId);

      const data = {won: wonPicId, loss: lossPicId};
      const headers= {'Content-Type': 'application/json'}
      axios.post("/api/rate", data, headers).then(response => { 
        console.log(response.data);
        this.call_pics();
      })
      .catch(error => {
        console.log(error.response);
      });

    }

  },
  
  created: function(){
    this.call_mashes();
  },
  mounted: function(){

  },
}
</script>


<style scoped>
.selectFrame{
  text-align: center;
  margin: 10px auto auto auto;
}
.selectFrame select{
  padding:6px;
  min-width: 280px;
  background-color: #444;
  color:#fff;
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  box-shadow: 1px 1px #fff;
}
.selectFrame .mashDesc{
  display: table;
  margin: auto;
  padding:12px;
  font-size: 16px;
  color:#333;
  text-shadow: 1px 1px #fff;
  font-weight: bold;
}
.selectFrame .sideBtn{
  min-width:130px;
  background-color: #444;
  color:#fff;
  text-align:center;
  font-size:16px;
  padding:7px;
  margin: auto auto auto 12px;
  *border-radius: 8px;
  border: none;
  box-shadow: 1px 1px #fff;
  cursor:pointer;
  font-family: 'Courier New', Courier, monospace;
}
.selectFrame .sideBtn:hover{
  background-color: #333;
}

.mashFrame{
  display: table;
  margin: 20px auto auto auto;
  background-color: #ccc;
  box-shadow: 1px 1px #fff;
  padding: 4px;
}
.mashFrame td{
  vertical-align: top;
}
.mashFrame img{
  margin:8px;
  box-shadow: 1px 1px #fff;
  cursor: pointer;
  border: 1px solid #999;
  max-width: 600px;
  max-height: 600px;
  width:96%;
}

</style>
