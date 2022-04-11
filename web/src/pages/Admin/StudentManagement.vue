<template lang="pug">
  div
    management-component(
      :title="'học sinh'"
    )
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { ManagementComponent } from 'components'

const StudentManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup() {
    return {}
  }
})

export default StudentManagement
</script>

<style lang="sass"></style>
