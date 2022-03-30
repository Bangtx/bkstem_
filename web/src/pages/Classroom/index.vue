<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(
        @on-click="onSelectFeature"
      )
      .w-full.border-l
        class-home(
          v-if="feature==='index'" :classroom="classroom" :students="students" :teacher="teacher"
        )
        roll-call(
          v-if="feature==='rollcall'" :classroom="classroom" :students="students" :teacher="teacher"
        )


</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { HeaderBar, MenuComponent } from 'components'
import { endpoints, toCamelCase } from 'utils'
import { api } from 'plugins'
import ClassHome from './ClassHome.vue'
import RollCall from './RollCall.vue'

interface Teacher {
  id: number
  name: string
}

interface ClassTime {
  dateOfWeek: string
  startTime: string
  stopTime: string
}

interface Student {
  id: number
  name: string
  dateOfBirth: string
  gender: string
}

interface ClassroomType {
  id: number
  name: string
  teacher: Teacher
  students: Student
  classTime: ClassTime
}

const Classroom = defineComponent({
  components: {
    HeaderBar,
    MenuComponent,
    ClassHome,
    RollCall
  },
  setup(props, { root }) {
    const { $toast, $route } = root
    const classroomID = $route.params.classroomId
    const feature = ref('index')
    const classroom = ref<ClassroomType | any>({})
    const students = ref<Array<Student>>([])
    const teacher = ref<Teacher | any>({})

    const onSelectFeature = (data: string) => {
      feature.value = data
    }
    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}${classroomID}`)
        classroom.value = toCamelCase(data)
        students.value = classroom.value.students
        teacher.value = classroom.value.teacher
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })
    return {
      onSelectFeature,
      students,
      classroom,
      teacher,
      feature
    }
  }
})

export default Classroom
</script>

<style lang="sass">
.menu-item
  cursor: pointer
.menu-item:hover
  background-color: #EEE
</style>
