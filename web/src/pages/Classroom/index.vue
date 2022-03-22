<template lang="pug">
  .bg-gray-50.min-h-screen
    header-bar
    .flex.flex-col.pt-18(class="md:flex-row")
      nav
        .bg-white.border-r.pb-2.fixed.bottom-0.z-10.w-full.content-center(class="md:bg-gray-50 md:relative md:h-screen md:w-60")
          .text-sm.content-center.text-left.justify-between(class="md:mt-12 md:w-60 md:fixed md:left-0 md:top-0 md:content-start")
            .list-reset.flex.justify-between.flex-row.pt-3.px-2.text-center.text-gray-600(class="md:flex-col md:py-3 md:px-2 md:text-left")
              .hidden.relative(class="md:block md:px-6 md:py-3 md:pt-6")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="index.html")
                  .flex.justify-center
                    svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6")
                  span(class="md:ml-4") Trang chủ
              .relative(class="md:px-6 md:py-3")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="diemdanh.html")
                  .flex.justify-center
                    svg.w-5.h-5(aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor")
                      path(d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01")
                  span(class="md:ml-4") Điểm danh
              .relative(class="md:px-6 md:py-3")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="lichhoc.html")
                  .flex.justify-center
                    svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z")
                  span(class="md:ml-4") Lịch học
              .relative(class="md:px-6 md:py-3")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="diemso.html")
                  .flex.justify-center
                    svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z")
                  span(class="md:ml-4") Điểm số
              .relative(class="md:px-6 md:py-3")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="ttht.html")
                  .flex.justify-center
                    svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                      path(d="M12 14l9-5-9-5-9 5 9 5z")
                      path(d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222")
                  spanhidden(class="md:ml-4 md:block") Tình hình học tập
                  span(class="md:hidden md:ml-4 md:block") THHT
              .relative(class="md:px-6 md:py-3")
                a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" href="dkh.html")
                  .flex.justify-center
                    svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                      path(stroke-linecap="round" stroke-linejoin="round" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122")
                  spanhidden(class="md:ml-4 md:block") Đăng kí học
                  span(class="md:ml-4 md:hidden") Đăng kí


</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { HeaderBar } from 'components'

const Classroom = defineComponent({
  components: {
    HeaderBar
  },
  setup() {
    return {}
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
