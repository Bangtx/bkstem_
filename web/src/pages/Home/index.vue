<template lang="pug">
  div
    header-bar
    banner.pl-3.pr-3.pb-3
    span {{ value }}
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import { HeaderBar, Banner } from 'components'

const Home = defineComponent({
  components: {
    HeaderBar,
    Banner
  },
  setup() {
    const value = ref('hhi')
    return {
      value
    }
  }
})
export default Home
</script>
