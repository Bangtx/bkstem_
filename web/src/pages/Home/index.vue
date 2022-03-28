<template lang="pug">
  div
    .bg-gray-50.min-h-screen
      header-bar
      .px-4.text-gray-800(class="md:px-8")
        .flex.items-center.gap-4.mt-8
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class="hover:bg-orange-300 focus:outline-none")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Thêm lớp
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(class="hover:bg-orange-300 focus:outline-none")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Button 2
        .flex.items-center.gap-2.py-4.mt-4
          svg.h-7.w-7(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
            path(stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16")
          .text-3xl Danh sách lớp
        // class list
        .grid.gap-6.mb-8(class="md:grid-cols-2 xl:grid-cols-4")
          div(
            v-for="classroom in classrooms"
            :key="classroom.id"
          )
            class-button(
              :class-name="classroom.name"
              :total-student="classroom.students.length"
              @on-click="openClassroom(classroom.id)"
            )

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { HeaderBar, ClassButton } from 'components'
import { urlPath, endpoints, toCamelCase } from 'utils'
import { api } from 'plugins'

const Home = defineComponent({
  components: {
    HeaderBar,
    ClassButton
  },
  setup(props, { root }) {
    const { $router, $toast } = root
    const classrooms = ref([])
    const openClassroom = (classroomId: number) => {
      $router.push({
        name: urlPath.CLASSROOM.name,
        params: {
          classroomId: String(classroomId)
        }
      })
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.CLASSROOM}`)
        classrooms.value = toCamelCase(data)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })
    return {
      openClassroom,
      classrooms
    }
  }
})
export default Home
</script>
