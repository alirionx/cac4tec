<template>
  <div class="stdForm" v-on:keyup.enter="submit_admin_pwd">
    <div class="hl">App Init - Set Admin Password</div>

    <input type="password" id="adminPwdIpt" placeholder="Enter Admin Password" v-model="adminPwdIpt" />
    <input type="password" id="adminPwdRep" placeholder="Repeate Admin Password" v-model="adminPwdRep" />
    
    <div class="btnFrame">
      <button v-on:click="submit_admin_pwd">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AppInit',
  props: {
    msg: String,
    callback: Function
  },
  data(){
    return{
      adminPwdIpt: "",
      adminPwdRep: ""
    }
  },
  methods:{
    submit_admin_pwd(){
      console.log(this.adminPwdIpt + ' : ' + this.adminPwdRep)
      if(this.adminPwdIpt == ""){
        let adminPwdIpt = document.getElementById("adminPwdIpt");
        var tmpColo = adminPwdIpt.style.borderColor;
        adminPwdIpt.style.borderColor = "red";
        setTimeout( function(){
          adminPwdIpt.style.borderColor = tmpColo;
        },400 )
        return false;
      }
      if(this.adminPwdIpt != this.adminPwdRep){
        let adminPwdRep = document.getElementById("adminPwdRep");
        var tmpColo = adminPwdRep.style.borderColor;
        adminPwdRep.style.borderColor = "red";
        setTimeout( function(){
          adminPwdRep.style.borderColor = tmpColo;
        },400 )
        return false;
      }

      const data = {pwd: this.adminPwdIpt}
      const headers= {'Content-Type': 'application/json'}
      axios.post("/api/app/init", data, headers).then(response => { 
        console.log(response.data);
        this.callback();
      })
      .catch(error => {
        console.log(error);
        this.adminPwdIpt = "";
        this.adminPwdRep = "";
      });
      
    },

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
