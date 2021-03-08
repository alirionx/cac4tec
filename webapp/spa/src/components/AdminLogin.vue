<template>
  <div class="stdForm" v-on:keyup.enter="submit_login">
    <div class="hl">Admin Login</div>

    <input type="password" id="adminPwdIpt" placeholder="Enter Admin Password" v-model="adminPwd" />
    
    <div class="btnFrame">
      <button v-on:click="submit_login">login</button>
      <button v-on:click="cancel_login">cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLogin',
  props: {
    msg: String,
    callback: Function
  },
  data(){
    return{
      adminPwd: ""
    }
  },
  methods:{
    submit_login(){
      if(this.adminPwd == ""){
        let adminPwdIpt = document.getElementById("adminPwdIpt");
        var tmpColo = adminPwdIpt.style.borderColor;
        adminPwdIpt.style.borderColor = "red";
        setTimeout( function(){
          adminPwdIpt.style.borderColor = tmpColo;
        },400 )
        return false;
      }

      const data = {pwd: this.adminPwd}
      const headers= {'Content-Type': 'application/json'}
      axios.post("/api/auth", data, headers).then(response => { 
        console.log(response.data);
        this.callback();
      })
      .catch(error => {
        console.log(error);
        this.adminPwd = "";
      });
    },

    cancel_login(){
      location.hash = '/';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.stdForm{
  margin-top: 10vh;
}
input[type=password]{
  margin-top:16px;
  text-align: center;
  font-weight: normal;
}

</style>
