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
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

import ActionMenu from '../components/ActionMenu.vue'

export default {
  name: 'Admin',
  components: {
    ActionMenu
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
          manda: true
        },
        {
          col: "name",
          hl: "Mash Name",
          align: "left",
          type: "input",
          manda: true
        },
        {
          col: "description",
          hl: "Mash Description",
          align: "left",
          type: "input",
          manda: false
        }
      ],
      
      actDefi:[
        {
          txt: "edit",
          fw: this.call_edit
        },
        {
          txt: "delete",
          fw: this.call_delete
        }
      ]
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

    call_edit(idx){
      console.log("call_edit: "+idx)
    },
    call_delete(idx){
      console.log("call_delete: "+idx)
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