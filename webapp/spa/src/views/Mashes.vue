<template>
  <div class="Mashes">
    <select v-on:change="call_mash" v-model="selected_mash" v-if="mashes.length>0">
      <option v-if="selected_mash==null" value="null">Please select a mash</option>
      <option v-for="(mash, idx) in mashes" :key="idx" :value="idx">{{mash.name}}</option>
    </select>
    <div class="mashDesc" v-if="selected_mash!=null">{{selected_mash_desc}}</div>
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

  },
  
  created: function(){
    this.call_mashes();
  },
  mounted: function(){

  },
}
</script>


<style scoped>
select{
  padding:6px;
  min-width: 280px;
  background-color: #444;
  color:#fff;
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  box-shadow: 1px 1px #fff;
}
.mashDesc{
  display: table;
  margin: auto;
  padding:12px;
  font-size: 16px;
  color:#333;
  text-shadow: 1px 1px #fff;
  font-weight: bold;
}
</style>
