<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col(class="md:flex-row")
      menu-component(
        :is-admin="false"
        @on-click="onSelectFeature"
      )
      .w-full.border-l
        class-home(
          v-if="feature==='index'"
          :classroom="classroom"
          :students="students"
          :teacher="teacher"
          :units="units"
        )
        roll-call(
          v-if="feature==='rollcall'" :classroom="classroom" :students="students" :teacher="teacher"
        )
        schedule(
          v-if="feature==='schedule'"
        )
        score(
          v-if="feature==='score'" :classroom="classroom" :students="students"
        )
        learn(
          v-if="feature==='learn'" :classroom="classroom" :students="students"
        )
        notification-student(
          v-if="feature==='noti'" :classroom="classroom"
        )
        home-work(
          v-if="feature==='home_work'" :classroom="classroom" :units="units"
        )

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { HeaderBar, MenuComponent } from 'components'
import { endpoints, toCamelCase } from 'utils'
import { api } from 'plugins'
import ClassHome from './ClassHome.vue'
import RollCall from './RollCall.vue'
import Schedule from './Schedule.vue'
import Score from './Score.vue'
import Learn from './Learn.vue'
import NotificationStudent from './NotificationStudent.vue'
import HomeWork from './HomeWork.vue'

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
    RollCall,
    Schedule,
    Score,
    Learn,
    NotificationStudent,
    HomeWork
  },
  setup(props, { root }) {
    const { $toast, $route } = root
    const classroomID = $route.params.classroomId
    const feature = ref('index')
    const classroom = ref<ClassroomType | any>({})
    const students = ref<Array<Student>>([])
    const teacher = ref<Teacher | any>({})
    const units = ref<any[]>([])

    const onSelectFeature = (data: string) => {
      feature.value = data
    }

    const getSchedule = async () => {
      try {
        const { data } = await api.get(`${endpoints.SCHEDULE}?classroom=${classroomID}`)
        units.value = toCamelCase(data)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}${classroomID}`)
        classroom.value = toCamelCase(data)
        students.value = classroom.value.students
        teacher.value = classroom.value.teacher

        await getSchedule()
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
      feature,
      units
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
