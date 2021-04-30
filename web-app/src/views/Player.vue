<template>
      <div class="text-center">
        <v-bottom-sheet
        v-model="openPlayer"
          inset
          hide-overlay
          persistent
          no-click-animation
          :retain-focus="false"
        >
          <template >
          </template>
          <v-card tile>
            <v-progress-linear
              :value="progress"
              :indeterminate="progress == 0"
              class="my-0"
              height="3"
            ></v-progress-linear>

            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>{{title}}</v-list-item-title>
                  <v-list-item-subtitle>{{progressString}}</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-icon>
                  <v-btn icon @click="sync">
                    <v-icon>mdi-cast-audio</v-icon>
                  </v-btn>
                </v-list-item-icon>
                <v-spacer></v-spacer>

                <v-list-item-icon>
                  <v-btn icon>
                    <v-icon>mdi-rewind</v-icon>
                  </v-btn>
                </v-list-item-icon>

                <v-list-item-icon
                  :class="{ 'mx-5': $vuetify.breakpoint.mdAndUp }"
                >
                  <v-btn icon @click="icon == 'mdi-pause' ? pause() : play()">
                    <v-icon>{{icon}}</v-icon>
                  </v-btn>
                </v-list-item-icon>

                <v-list-item-icon
                  class="ml-0"
                  :class="{ 'mr-3': $vuetify.breakpoint.mdAndUp }"
                >
                  <v-btn icon>
                    <v-icon>mdi-fast-forward</v-icon>
                  </v-btn>
                </v-list-item-icon>
              </v-list-item>
            </v-list>
          </v-card>
        </v-bottom-sheet>
      </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Player",
  props: {
    openPlayer: Boolean,
  },
  data: () => ({
   status:null,
  }),
  mounted : function () {
  this.refresh()
  },
  computed: {
    title: function () { 
      let result = "Unknown"
      if ((this.status != null) && (this.status.title != null) && (this.status.title != undefined)) {
        result = this.status.title
      } 
      return result
    },
    progress: function () { 
      let result = 0
      if ((this.status != null) && (this.status.current_time != null) && (this.status.current_time != undefined)) {
        result = this.status.current_time * 100/this.status.duration
      } 
      return result
    },
    progressString: function () { 
      let result = ""
      if ((this.status != null) && (this.status.current_time != null) && (this.status.current_time != undefined)) {
        result = `${this.status.current_time} : ${this.status.duration}`
      } 
      return result
    }, 
    icon: function() {
      let result = "mdi-pause"
      if ((this.status != null) && (this.status.player_state != null) && (this.status.player_state != undefined)) {
        this.status.player_state == 'PLAYING' ? result = "mdi-pause" : result = "mdi-play" 
      } 
      return result
    }
  },
  watch : {

  },
  methods: {
    getStatus: function () {
      axios
      .get(`http://127.0.0.1:5000/api/status`)
      .then((response) => {
        console.log(response);
        this.status = response.data
      })
      .catch((e) => {
        console.log(e);
      });
    },
    refresh: function() {
      setInterval(() => {
        if (this.openPlayer){
          this.getStatus()
        }
      }, 5000);
    },
    pause: function () {
      axios
      .get(`http://127.0.0.1:5000/api/pause`)
      .then((response) => {
        console.log(response);
      })
      .catch((e) => {
        console.log(e);
      });
    }, 
    play: function () {
      axios
      .get(`http://127.0.0.1:5000/api/sync`)
      .then((response) => {
        console.log(response);
      })
      .catch((e) => {
        console.log(e);
      });
    }, 
    sync: function () {
      axios
      .get(`http://127.0.0.1:5000/api/sync`)
      .then((response) => {
        console.log(response);
      })
      .catch((e) => {
        console.log(e);
      });
    }
  }
};
// 'current_time':status.current_time, 'duration':status.duration})
</script>
