<template>
  <div class="blocker">
    <div class="stdForm" v-on:keyup.enter="submit_reset_admin_pwd">
      <div class="hl">Reset Admin Password</div>

      <input type="password" id="curPwdIpt" placeholder="Enter current Admin Password" v-model="curPwdIpt" />
      <input type="password" id="newPwdIpt" placeholder="Enter new Admin Password" v-model="newPwdIpt" />
      <input type="password" id="repPwdIpt" placeholder="Repeate new Admin Password" v-model="repPwdIpt" />
      
      <div class="btnFrame">
        <button v-on:click="submit_reset_admin_pwd">Submit</button>
        <button v-on:click="callback">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminPwd',
  props: {
    msg: String,
    callback: Function
  },
  data(){
    return{
      curPwdIpt: "",
      newPwdIpt: "",
      repPwdIpt: ""
    }
  },
  methods:{
    submit_reset_admin_pwd(){
      let idList = ["curPwdIpt", "newPwdIpt", "repPwdIpt"]
      for(let idx in idList){
        if(this[idList[idx]] == ""){
          let curDomEl = document.getElementById(idList[idx]);
          var tmpColo = curDomEl.style.borderColor;
          curDomEl.style.borderColor = "red";
          setTimeout( function(){
            curDomEl.style.borderColor = tmpColo;
          },400 )
          return false;
        }
      }
     
      if(this.newPwdIpt != this.repPwdIpt){
        let repPwdIpt = document.getElementById("repPwdIpt");
        var tmpColo = repPwdIpt.style.borderColor;
        repPwdIpt.style.borderColor = "red";
        setTimeout( function(){
          repPwdIpt.style.borderColor = tmpColo;
        },400 )
        this.repPwdIpt = "";
        return false;
      }

      const data = {
        curPwd: this.curPwdIpt,
        newPwd: this.newPwdIpt,
      }
      const headers= {'Content-Type': 'application/json'}
      axios.post("/api/app/pwd", data, headers).then(response => { 
        console.log(response.data);
        this.callback();
      })
      .catch(error => {
        console.log(error);
        this.curPwdIpt = "";
        this.newPwdIpt = "";
        this.repPwdIpt = "";
        let curPwdIpt = document.getElementById("curPwdIpt");
        var tmpColo = curPwdIpt.style.borderColor;
        curPwdIpt.style.borderColor = "red";
        setTimeout( function(){
          curPwdIpt.style.borderColor = tmpColo;
        },400 )
      });
    },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stdForm{
  margin-top: 16vh;
}
input[type=password]{
  margin-top:16px;
  text-align: center;
  font-weight: normal;
}

</style>
