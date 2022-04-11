<template lang="pug">
  div
    management-component(
      :title="'giáo viên'"
    )
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { ManagementComponent } from 'components'

const TeacherManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup() {
    return {}
  }
})

export default TeacherManagement
</script>

<style lang="sass"></style>
