<template>
  <div id="app">
    <div class="headBlock">
      <div class="hl" v-on:click="call_home">PicMash Example App 4 TechSession</div>
      <img class="gear" v-bind:class="{active: chk_admin_hash()}" src="@/assets/admin_gear.svg" v-on:click="call_admin" />
    </div>

    <router-view v-if="appReady" />

    <AppInit v-if="!appReady" 
      v-bind:callback="chk_app_ready" />

  </div>
</template>

<script>
import axios from 'axios'
import AppInit from './components/AppInit.vue'

export default {
  name: 'App',
  components:{
    AppInit
  },
  data(){
    return{
      appReady: false,
    }
  },
  methods:{
    chk_app_ready(){
      axios.get("/api/app/init").then(response => { 
        console.log(response.data);
        this.appReady = response.data.state;
      })
      .catch(error => {
        console.log(error);
      });
    },
    call_admin(){   
      if(this.chk_admin_hash()){
        this.call_home();
        return
      }
      location.hash = "/admin";
    },
    call_home(){
      location.hash = "/";
    },
    chk_admin_hash(){
      if(location.hash == '#/admin'){
        return true;
      }
      else{
        return false;
      }
    },
  },

  created: function(){
    this.chk_app_ready();
  }
}
</script>


<style>
body {
  background-image: linear-gradient(#ddd 100%, #bbb 100%);
  background-repeat: no-repeat;
  background-color: #ddd;
  *font-family: Avenir, Helvetica, Arial, sans-serif;
  font-family: 'Courier New', Courier, monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  padding: 100px 8px 8px 8px;
  min-height:80vh;
}
.headBlock{
  position: fixed;
  top: 0px;
  left: 0px;
  width: 97%;
  text-align: center;
  padding: 30px;
  background-color: #ccc;
  box-shadow: 0px 2px 4px #555;
  border: 1px solid #444;
  z-index: 10;
}
.headBlock .hl{
  font-size: 24px;
  color:#333;
  text-shadow: 1px 1px #fff;
  font-weight: 900;
  font-family: 'Courier New', Courier, monospace;
  cursor: pointer;
}
.headBlock .gear{
  position: absolute;
  right:50px;
  top:22px;
  height: 40px;
  cursor: pointer;
  padding-bottom:4px;
}
.headBlock .gear:hover{
  border-bottom: #333 2px solid;
}
.headBlock .active{
  border-bottom: #333 2px solid;
}

.pageHl{
  padding:10px;
  font-size: 22px;
  color:#333;
  text-shadow: 1px 1px #fff;
  *font-weight: bold;
}

.stdTbl{
  margin: 30px auto 30px auto;
  min-width: 800px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 20px;
  *font-weight: 900;
}
.stdTbl th{
  padding:6px;
  background-color: #444;
  color:#fff;
  box-shadow: 1px 1px #fff;
  font-weight: normal;
}
.stdTbl th:last-child{
  text-align: center;
}
.stdTbl td{
  padding:6px;
  background-color: none;
  color:#333;
  text-shadow: 1px 1px #fff;
  font-weight: bold;
  border: 1px solid #444;
  box-shadow: 1px 1px #fff;
}
.stdTbl td img{
  margin:-4px;
  max-height: 50px;
  cursor: pointer;
  box-shadow: 1px 1px #fff;
}
.stdTbl td:last-child{
  text-align: center;
}
.stdTbl .noBorders td{
  border: none;
  box-shadow: none;
  height: 40px;
}
.stdTbl button{
  min-width: 50px;
  margin: -6px;
  background-color: #444;
  color:#fff;
  text-align:center;
  font-size:15px;
  padding:3px;
  border: none;
  box-shadow: 1px 1px #fff;
  cursor:pointer;
  font-family: 'Courier New', Courier, monospace;
}
.stdTbl button:hover{
  background-color: #333;
}

.blocker{
  position: fixed;
  top:0px;
  left:0px;
  width:100%;
  height: 100vh;
  z-index: 2;
  background-image: linear-gradient(#cfcfcf 100%, #bbb 100%);
  background-repeat: no-repeat;
}

.stdForm{
  display: table;
  margin: 18vh auto auto auto;
  min-width:500px;
  min-height:100px;
  text-align:left;
  padding:14px;
  border: 1.5px solid #444;
  *border-radius: 12px;
  box-shadow: 1px 1px #fff;
  *background-color:#bbb;
}
.stdForm .hl{
  background-color: #444;
  color:#fff;
  text-align:center;
  font-size:14px;
  font-weight:bold;
  padding:8px;
  *border-radius: 6px;
  *border: 1px solid rgb(2, 22, 2);
  box-shadow: 1px 1px #fff;
  margin:auto auto 6px auto;
}
.stdForm .iptHl{
  text-align: left;
  font-size:14px;
  font-weight:bold;
  color: #000;
  padding:18px 8px 4px 2px;
}
.stdForm input[type=text],input[type=password]{
  text-align: left;
  font-size:16px;
  color: #000;
  padding:6px;
  margin: 0px 0px 8px 2px;
  border: 1px solid #777;
  background-color:#eee;
  font-family: 'Courier New', Courier, monospace;
  box-shadow: 1px 1px #fff;
  width:95%;
  font-weight: 900;
}
.stdForm input[type=text]:focus,input[type=password]:focus{
  background-color: #f8f8f8;
}
.stdForm input[type=text][disabled]{
  background-color:#ccc;
}
.stdForm .btnFrame{
  text-align: center;
  padding:26px 0px 2px 0px;
}
.stdForm .btnFrame button{
  min-width:120px;
  background-color: #444;
  color:#fff;
  text-align:center;
  font-size:18px;
  padding:5px;
  margin: auto 12px auto 12px;
  *border-radius: 8px;
  border: none;
  box-shadow: 1px 1px #fff;
  cursor:pointer;
  font-family: 'Courier New', Courier, monospace;
}
.stdForm .btnFrame button:hover{
  background-color: #333;
}
</style>
