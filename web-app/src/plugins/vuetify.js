import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.grey.darken3,
        secondary: colors.grey.lighten1,
        accent: colors.blue.darken3,
        error: colors.red.lighten1,
      },
      dark: {
        primary: colors.grey.darken3,
        secondary: colors.grey.darken1,
        accent: colors.grey.darken1,
        error: colors.red.lighten1,
      }
    },
    // dark: true
  }
});
