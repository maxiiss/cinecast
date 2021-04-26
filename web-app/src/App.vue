<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title class="title text-h4" >Cinecast</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <Home @openPlayer="getOpenPlayerStatus" />
      <Player :openPlayer="openPlayer"/>
    </v-main>
  </v-app>
</template>

<script>
import Home from "@/views/Home";
import Player from "@/views/Player";
export default {
  name: "App",

  components: {
    Home,
    Player,
  },

  data: () => ({
    status: null,
    openPlayer:false
  }),

  methods: {
    getOpenPlayerStatus(event) {
      console.log("data after child handle: ", event); // get the data after child dealing
      this.openPlayer = event
    },
  },
};
</script>
