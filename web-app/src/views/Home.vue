<template>
  <div id="home">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card flat height="50px">
            <v-alert
              :type="not_type"
              dismissible
              transition="slide-y-transition"
              text
              v-model="notification"
            >
              {{ not_message }}</v-alert
            >
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card :loading="dev_loading" :disabled="dev_loading" outlined>
            <v-card-title> Home Cinema Configuration </v-card-title>
            <v-card-text>
              <v-form v-model="valid1" ref="form1">
                <v-row>
                  <v-col cols="12">
                    <v-autocomplete
                      v-model="v_device"
                      :items="video_devices"
                      :rules="[(v) => !!v || 'Video device must be chosen']"
                      item-text="friendly_name"
                      label="Video Device"
                      return-object
                    ></v-autocomplete>
                  </v-col>
                  <v-col cols="12">
                    <v-autocomplete
                      v-model="a_device"
                      :items="audio_devices"
                      :rules="[(v) => !!v || 'Audio device must be chosen']"
                      item-text="friendly_name"
                      label="Audio Device"
                      return-object
                    ></v-autocomplete>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="setConfig()" color="accent">Validate</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card :disabled="!configValidated" outlined>
            <v-card-title> Media </v-card-title>
            <v-card-text>
              <v-form>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      label="Video url"
                      v-model="url"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="playUrl()" color="accent"
                ><v-icon>mdi-play</v-icon></v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",

  data: () => ({
    devices: [{}],
    dev_loading: true,
    v_device: null,
    a_device: null,
    url: "",
    valid1: false,
    configValidated: false,
    notification: false,
    not_message: "",
    not_type: "warning",
  }),
  computed: {
    video_devices: function () {
      return this.devices.filter((element) => element !== this.a_device);
    },
    audio_devices: function () {
      return this.devices.filter((element) => element !== this.v_device);
    },
  },
  created: function () {
    if (window.webpackHotUpdate) {
      this.url =
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4";
    }
    this.getDevices();
  },
  methods: {
    openPlayer: function () {
      this.$emit("openPlayer", true);
    },
    getDevices: function () {
      axios
        .get(`http://127.0.0.1:5000/api/devices`)
        .then((response) => {
          console.log(response);
          this.devices = response.data.devices;
          this.dev_loading = false;
        })
        .catch((e) => {
          console.error(e);
          this.not_message =
            "Unable to reach the backend. Please refresh the page";
          this.not_type = "error";
          this.notification = true;
        });
    },
    playUrl: function () {
      this.openPlayer();
      axios
        .post(`http://127.0.0.1:5000/api/playurl`, {
          url: this.url,
          v_device: this.v_device.friendly_name,
          a_device: this.a_device.friendly_name,
        })
        .then((response) => {
          this.openPlayer();
          console.log(response);
        })
        .catch((e) => {
          console.log(e);
        });
    },
    setConfig: function () {
      this.$refs.form1.validate();
      if (this.valid1) {
        axios
          .post(`http://127.0.0.1:5000/api/config`, {
            v_device: this.v_device.friendly_name,
            a_device: this.a_device.friendly_name,
          })
          .then((response) => {
            console.log(response);
            this.configValidated = true;
          })
          .catch((e) => {
            console.log(e);
            this.not_message =
              "Unable to control at least one device. You may try to restart the devices.";
            this.not_type = "error";
            this.notification = true;
            this.configValidated = false;
            this.$refs.form1.reset();
          });
      }
    },
  },
};
</script>

<style scoped>
#home {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-repeat: no-repeat;
}
</style>