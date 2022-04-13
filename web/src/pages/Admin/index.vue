<template lang="pug">
  div
    .bg-gray-50.min-h-screen
      header-bar(:isAdmin="true")
      .flex.flex-col(class="md:flex-row")
        menu-component(
          :is-admin="true"
          @on-click="onSelectFeature"
        )
        .w-full(class="md:border-l")
          teacher-management(
            v-if="feature === 'teacher_management'"
          )
          classroom-management(
            v-if="feature === 'class_management'"
          )
          student-management(
            v-if="feature === 'student_management'"
          )

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { HeaderBar, MenuComponent } from 'components'
import TeacherManagement from './TeacherManagement.vue'
import StudentManagement from './StudentManagement.vue'
import ClassroomManagement from './ClassroomManagement.vue'

const Admin = defineComponent({
  components: {
    HeaderBar,
    MenuComponent,
    TeacherManagement,
    ClassroomManagement,
    StudentManagement
  },
  setup() {
    const feature = ref('class_management')

    const onSelectFeature = (data: string) => {
      feature.value = data
    }
    return {
      feature,
      onSelectFeature
    }
  }
})

export default Admin
</script>

<style lang="sass"></style>
