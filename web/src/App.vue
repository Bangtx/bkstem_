<template lang="pug">
  div
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
