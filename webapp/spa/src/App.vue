<template>
  <div id="app">
    <div class="headBlock">
      <div class="hl" v-on:click="call_home">PicMash Example App 4 TechSession</div>
      <img class="gear" v-bind:class="{active: chk_admin_hash()}" src="@/assets/admin_gear.svg" v-on:click="call_admin" />
    </div>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods:{
    call_admin(){
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
    }
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
  padding: 80px 8px 8px 8px;
  min-height:80vh;
}
.headBlock{
  position: fixed;
  top: 0px;
  left: 0px;
  width: 95%;
  text-align: center;
  padding: 40px;
  *background-color: #000;
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
  right:60px;
  top:32px;
  height: 40px;
  cursor: pointer;
}
.headBlock .gear:hover{
  border-bottom: #333 2px solid;
}
.headBlock .active{
  border-bottom: #333 2px solid;
}

.stdTbl{
  margin: 30px auto auto auto;
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
.stdTbl td:last-child{
  text-align: center;
}
</style>
