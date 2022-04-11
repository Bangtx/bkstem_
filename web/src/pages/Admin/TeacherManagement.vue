<template lang="pug">
  div
    management-component(
      :title="'giáo viên'"
      :data="teachers"
      :classrooms="classrooms"
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

const TeacherManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const teachers = ref<Teacher[]>([])
    const classrooms = ref<ClassroomType[]>([])

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.TEACHER}`),
          api.get(`${endpoints.CLASSROOM}`)
        ])
        const [{ data: teacherData }, { data: classData }] = data
        teachers.value = toCamelCase(teacherData)
        classrooms.value = toCamelCase(classData)
      } catch {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })

    return {
      teachers,
      classrooms
    }
  }
})

export default TeacherManagement
</script>

<style lang="sass"></style>
