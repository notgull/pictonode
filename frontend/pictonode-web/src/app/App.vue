<!-- GNU AGPL v3 License -->

<!--
  This file in its entirety was written by John Nunley and Grace Meredith.
-->

<script lang="ts">
import { defineComponent } from "vue";
import RenderedView from "./RenderedView.vue";
import Topbar from "./Topbar.vue";
import Widgets from "./Widgets.vue";

export default defineComponent({
  components: { RenderedView, Topbar, Widgets },
});
</script>

<template>
  <v-app :id="'pictonode'">
    <Topbar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
