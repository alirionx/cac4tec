<template>
  <div class="blocker">
    <div class="stdForm" v-on:keyup.enter="submit_confirm">
      
      <div class="hl">{{msg}}</div>

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
      this.fw();
      this.callback();
    }
  },
  mounted: function(){
  
  }
}
</script>

<style scoped>

</style>
