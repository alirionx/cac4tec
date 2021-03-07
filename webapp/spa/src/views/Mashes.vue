<template>
  <div class="Mashes">
    <div class="selectFrame">
      <select v-on:change="call_mash" v-model="selected_mash" v-if="mashes.length>0">
        <option v-if="selected_mash==null" value="null">Please select a mash</option>
        <option v-for="(mash, idx) in mashes" :key="idx" :value="idx">{{mash.name}}</option>
      </select>
      <button class="sideBtn" v-if="selected_mash!=null" v-on:click="call_rating">show rating</button>
      <div class="mashDesc" v-if="selected_mash!=null">{{selected_mash_desc}}</div>
    </div>  
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
    
    call_mash(){
      this.selected_mash_desc = this.mashes[this.selected_mash].description;
      console.log(this.selected_mash + " calling...")
    },

    call_rating(){
      location.hash = "/pics/"+this.mashes[this.selected_mash].id
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
</style>
