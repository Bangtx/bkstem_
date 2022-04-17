<template lang="pug">
  div
    management-component(
      :title="'học sinh'"
      :data="students"
      :classrooms="classrooms"
      @reload="reload()"
    )
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { ManagementComponent } from 'components'
import { api } from 'plugins'
import { toCamelCase, endpoints } from 'utils'

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
  notification?: string[]
}

interface ClassroomType {
  id: number
  name: string
  teacher: Teacher
  students: Student
  classTime: ClassTime
}

const StudentManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup(props, { root }) {
    const { $toast } = root
    const students = ref<Student[]>([])
    const classrooms = ref<ClassroomType[]>([])

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.STUDENT}`),
          api.get(`${endpoints.CLASSROOM}`)
        ])
        const [{ data: studentData }, { data: classData }] = data
        students.value = toCamelCase(studentData)
        classrooms.value = toCamelCase(classData)
      } catch {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
    }

    onMounted(async () => {
      await getData()
    })

    return {
      students,
      classrooms,
      reload
    }
  }
})

export default StudentManagement
</script>

<style lang="sass"></style>
