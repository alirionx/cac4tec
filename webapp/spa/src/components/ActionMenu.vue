<template>
  <div class="ActionMenu">
    <div class="dotFrame" v-on:click="set_active_mash(idx)" tag="menu">
      <div tag="menu"></div>
      <div tag="menu"></div>
      <div tag="menu"></div>
    </div>

    <div class="actFrame" v-if="idx==active_mash">
      <div v-for="(act, actidx) in actDefi" :key="actidx" v-on:click="act.fw(idx)">{{act.txt}}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActionMenu',
  props: {
    idx: Number,
    active_mash: Number,
    set_active_mash: Function,
    actDefi: Array
  },
  data(){
    return{
      
    }
  },
  methods:{
    
  },
  mounted: function(){
  
  }
}
</script>

<style scoped>
.ActionMenu{
  position: relative;
}
.ActionMenu .dotFrame{
  display: inline-block;
  border: 1px solid #444;
  border-radius: 4px;
  text-align: center;
  box-shadow: 1px 1px #fff;
  margin:-2px auto -8px auto;
  cursor: pointer;
}
.ActionMenu .dotFrame:hover div{
  background-color: #000;
}
.ActionMenu .dotFrame div{
  width:14px;
  height: 6px;
  border-radius: 3px;
  background-color:  #444;
  box-shadow: 1px 1px #fff;
  margin:2px;
}

.ActionMenu .actFrame{
  position: absolute;
  left:50px;
  top:0px;
  z-index: 10;
  min-width: 100px;
}
.ActionMenu .actFrame div{
  padding:4px;
  text-align: left;
  background-color: #444;
  color: #fff;
  font-size: 14px;
  font-weight: normal;
  text-shadow: none;
  white-space: nowrap;
  border:1px solid #fff;
  margin-bottom: -1px;
  cursor: pointer;
}
.ActionMenu .actFrame div:hover{
  background-color: #222;
}
</style>
