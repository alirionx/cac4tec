<template>
  <div class="admin">
    <table class="stdTbl">
      <thead>
        <tr>
          <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign:col.align}">{{col.hl}}</th>
          <th>Act</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in mashes" :key="idx">
          <td v-for="(col, idx) in defi" :key="idx" :style="{textAlign:col.align}">{{row[col.col]}}</td>
          <td>
            <ActionMenu 
              v-bind:idx="idx" 
              v-bind:active_mash="active_mash" 
              v-bind:set_active_mash="set_active_mash" 
              v-bind:actDefi="actDefi" />
          </td>
        </tr>

        <tr class="noBorders">
          <td :colspan="defi.length"></td>
          <td> 
            <button v-on:click="call_add">add</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="blocker" v-if="activeAction=='edit'||activeAction=='add'">
      <div class="stdForm" v-on:keyup.enter="submit_mash_changes">
        <div class="hl">{{activeAction}} piture mash</div>

        <div v-for="(col, idx) in defi" :key="idx">
          <div class="iptHl">{{col.hl}}:</div>
            <input v-if="col.type=='static'" type="text" disabled v-model="activeRow[col.col]" />
            <input :id="'change_'+col.col" v-if="col.type=='text'" type="text" v-model="activeRow[col.col]" />
        </div>

        <div class="btnFrame">
          <button v-on:click="submit_mash_changes">ok</button>
          <button v-on:click="reset_active_action">cancel</button>
        </div>
      </div>
    </div>

    <ConfirmBox v-if="confirmMsg!=null"
      v-bind:msg = confirmMsg
      v-bind:callback = reset_confirm
      v-bind:fw = confirmFw
    />

  </div>
</template>

<script>
import axios from 'axios'

import ActionMenu from '../components/ActionMenu.vue'
import ConfirmBox from '../components/ConfirmBox.vue'

export default {
  name: 'Admin',
  components: {
    ActionMenu,
    ConfirmBox
  },
  data(){
    return{
      active_mash: null,
      mashes: [],
      defi:[
        {
          col: "id",
          hl: "DBId",
          align: "center",
          type: "static",
          manda: false
        },
        {
          col: "name",
          hl: "Mash Name",
          align: "left",
          type: "text",
          manda: true
        },
        {
          col: "description",
          hl: "Mash Description",
          align: "left",
          type: "text",
          manda: false
        }
      ],

      activeAction: "",
      activeMash: null,
      activeRow: {},
      
      actDefi:[
        {
          txt: "edit",
          fw: this.call_edit
        },
        {
          txt: "pics",
          fw: this.call_pics
        },
        {
          txt: "delete",
          fw: this.call_delete
        }
      ],

      confirmMsg: null,
      confirmFw: ()=>{},

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

    set_active_mash(idx){
      this.active_mash = idx;
    },
    reset_active_mash(){
      this.active_mash = null;
    },

    call_add(){
      this.activeAction = "add";
    },
    call_edit(idx){
      console.log("call_edit: "+idx);
      this.activeAction = "edit";
      this.activeMash = idx;
      this.activeRow = this.mashes[idx]
    },
    call_delete(idx){
      console.log("call_delete: "+idx);
      this.confirmMsg = "Do you really want do delete "+this.mashes[idx].name+"?";
      var fwFunc = this.delete_mash;
      this.confirmFw = function(){ fwFunc(idx) }
    },
    reset_active_action(){
      this.activeAction = "";
      this.activeMash = null;
      this.activeRow = {};
    },
    
    call_pics(idx){
      let id = this.mashes[idx].id;
      location.hash = '/pics/'+id;
    },

    submit_mash_changes(){
      for(var prop in this.defi){
        let curDefi = this.defi[prop]
        console.log(this.activeRow[curDefi.col]);
        if(curDefi.manda && this.activeRow[curDefi.col] == ""){
          let curIpt = document.getElementById('change_'+curDefi.col);
          var tmpColo = curIpt.style.borderColor;
          curIpt.style.borderColor = "red";
          setTimeout( function(){
            curIpt.style.borderColor = tmpColo;
          },400 )
          return false;
        }
      }

      if(this.activeAction == "add"){
        var meth = axios.post;
      }
      else if(this.activeAction == "edit"){
        var meth = axios.put;
      }
      else{
        return false;
      }
      const headers= {'Content-Type': 'application/json'}
      meth("/api/mash", this.activeRow, headers).then(response => { 
        console.log(response.data);
        this.call_mashes();
        this.reset_active_action();
      })
      .catch(error => {
        console.log(error);
      });
    },

    delete_mash(idx){
      let id = this.mashes[idx].id;

      //const headers = {'Content-Type': 'application/json'}
      //const data = {'id': id}
      //axios.delete("/api/mash/"+id, data, headers).then(response => { 
      axios.delete("/api/mash/"+id ).then(response => { 
        console.log(response.data);
        this.call_mashes();
      })
      .catch(error => {
        console.log(error);
      });
    },

    reset_confirm(){
      this.confirmMsg = null;
    }

  },
  
  created: function(){
    this.call_mashes();
  },
  mounted: function(){
    //UIUIUIUIUIUIU
    var fwFunc = this.reset_active_mash;
    document.body.addEventListener("click", function(ev){
      if(ev.target.getAttribute("tag") != 'menu'){
        fwFunc();
      }
    });
  },
}
</script>


<style scoped>
table tr:last-child td{
  border: none;
}

</style>