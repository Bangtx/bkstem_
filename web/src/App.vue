<template lang="pug">
  v-app
    router-view
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const App = defineComponent({
  props: {},
  setup() {
    return {}
  }
})
export default App
</script>

<style lang="sass">
@import 'styles/master.sass'
</style>

<style>
@import 'styles/css/main.css';
</style>
