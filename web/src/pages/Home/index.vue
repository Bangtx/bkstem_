<template lang="pug">
  div
    .bg-gray-50.min-h-screen
      header-bar
      .px-4.pt-24(class="md:px-8")
        .rounded-lg
          img.hidden.w-full.h-auto.rounded-lg(class="md:block" src="https://scontent.fhan15-2.fna.fbcdn.net/v/t1.15752-9/273590583_1134579140676320_8895692069881215157_n.png?stp=dst-png_s2048x2048&_nc_cat=104&ccb=1-5&_nc_sid=ae9488&_nc_ohc=wZrp74SfU_YAX-1c9I1&_nc_ht=scontent.fhan15-2.fna&oh=03_AVIBbSc9J3qVFLdc6P2dkz_8VS7LI7x5RSPaQUcD7V5ZBw&oe=625DB260" alt="")
          img.w-full.h-auto.rounded-lg(class="md:hidden" src="https://scontent.fhan15-2.fna.fbcdn.net/v/t1.15752-9/273590583_1134579140676320_8895692069881215157_n.png?stp=dst-png_s2048x2048&_nc_cat=104&ccb=1-5&_nc_sid=ae9488&_nc_ohc=wZrp74SfU_YAX-1c9I1&_nc_ht=scontent.fhan15-2.fna&oh=03_AVIBbSc9J3qVFLdc6P2dkz_8VS7LI7x5RSPaQUcD7V5ZBw&oe=625DB260" alt="")
        .flex.items-center.gap-4.mt-8
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-purple-600.border.border-transparent.rounded-lg(class="active:bg-purple-600 hover:bg-purple-700 focus:outline-none focus:shadow-outline-purple")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Thêm lớp
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-purple-600.border.border-transparent.rounded-lg(class="active:bg-purple-600 hover:bg-purple-700 focus:outline-none focus:shadow-outline-purple")
            svg.h-6.w-6(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
              path(stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6")
            span.text-base Button 2
        h1.text-3xl.py-4.mt-4 Danh sách lớp
        // class list
        .grid.gap-6.mb-8(class="md:grid-cols-2 xl:grid-cols-4")
          // Card
          class-button(@on-click="openClassroom()")
          //class-button
          //class-button
          //class-button
          //class-button
          //class-button

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { HeaderBar, ClassButton } from 'components'
import { urlPath } from 'utils'

const Home = defineComponent({
  components: {
    HeaderBar,
    ClassButton
  },
  setup(props, { root }) {
    const { $router } = root
    const openClassroom = () => {
      $router.push({
        path: urlPath.CLASSROOM.path
      })
      console.log('hih')
    }
    return {
      openClassroom
    }
  }
})
export default Home
</script>
