<template lang="pug">
  div
    management-component(
      :title="'lớp học'"
      :data="classrooms"
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

const ClassroomManagement = defineComponent({
  components: {
    ManagementComponent
  },
  setup(props, { root }) {
    const { $toast } = root
    const classrooms = ref<ClassroomType[]>([])

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}`)
        classrooms.value = toCamelCase(data)
      } catch {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })

    return {
      classrooms
    }
  }
})

export default ClassroomManagement
</script>

<style lang="sass"></style>
