<template lang="pug">
  div
    management-component(
      :title="'lớp học'"
    )
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { ManagementComponent } from 'components'

const ClassroomManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup() {
    return {}
  }
})

export default ClassroomManagement
</script>

<style lang="sass"></style>
