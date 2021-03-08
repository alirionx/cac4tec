<template>
  <div class="blocker">
    <div class="stdForm" v-on:keyup.enter="submit_confirm">
      
      <div class="hl">{{msg}}</div>
      <input type="text" id="hiddenFocus" />

      <div class="btnFrame">
        <button v-on:click="submit_confirm">ok</button>
        <button v-on:click="callback">cancel</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmBox',
  props: {
    msg: String,
    callback: Function,
    fw: Function
  },
  data(){
    return{
      
    }
  },
  methods:{
    submit_confirm(){
      console.log("submit_confirm");
      this.fw();
      this.callback();
    }
  },
  mounted: function(){
    let hiddenFocus = document.getElementById("hiddenFocus");
    hiddenFocus.focus();
  }
}
</script>

<style scoped>

#hiddenFocus{
  opacity: 0;
  height: 1px;
  padding:0px;
  font-size: 4px;
  margin-bottom: -10px;
}
</style>
