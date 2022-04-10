<template lang="pug">
  div
    .bg-white.border-r.pb-2.fixed.bottom-0.z-10.w-full.content-center(class="md:bg-gray-50 md:relative md:h-screen md:w-60")
      .text-sm.content-center.text-left.justify-between(class="md:mt-12 md:w-60 md:fixed md:left-0 md:top-0 md:content-start")
        .list-reset.flex.justify-between.flex-row.pt-3.px-2.text-center.text-gray-600(class="md:flex-col md:py-3 md:px-2 md:text-left")
          .relative(class="md:block md:px-6 md:py-3 md:pt-6")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', 'index')")
              .flex.justify-center
                svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6")
              span.hidden(class="md:ml-4 md:block") Trang chủ
              span(class="md:hidden ") T.Chủ
          .relative(class="md:px-6 md:py-3")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', 'rollcall')")
              .flex.justify-center
                svg.w-5.h-5(aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor")
                  path(d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01")
              span.hidden(class="md:ml-4 md:block") Điểm danh
              span(class="md:hidden") Đ.Danh
          .relative(class="md:px-6 md:py-3")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', 'score')")
              .flex.justify-center
                svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z")
              span(class="md:ml-4") Điểm số
          .relative(v-if="member.typeMember === 'teacher'" class="md:px-6 md:py-3")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', 'learn')")
              .flex.justify-center
                svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                  path(d="M12 14l9-5-9-5-9 5 9 5z")
                  path(d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222")
              span.hidden(class="md:ml-4 md:block") Tình hình học tập
              span(class="md:hidden ") THHT
          .relative(v-if="member.typeMember === 'student'" class="md:px-6 md:py-3")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800" @click="$emit('on-click', 'noti')")
              .flex.justify-center
                svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                  path(d="M12 14l9-5-9-5-9 5 9 5z")
                  path(d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222")
              span.hidden(class="md:ml-4 md:block") Thông báo
              span(class="md:hidden") T.Báo
          .relative(v-if="member.typeMember === 'teacher'" class="md:px-6 md:py-3")
            a.items-center.w-full.font-semibold.transition-colors.duration-150(class="md:inline-flex hover:text-gray-800"  @click="$emit('on-click', 'home_work')")
              .flex.justify-center
                svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z")
                  path(stroke-linecap="round" stroke-linejoin="round" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z")
              span.hidden(class="md:ml-4 md:block") Giao bài tập
              span(class="md:hidden ") Bài tập

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { toCamelCase } from 'utils'
import jwtDecode from 'jwt-decode'

const MenuComponent = defineComponent({
  setup() {
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    return {
      member
    }
  }
})

export default MenuComponent
</script>

<style lang="sass">
.relative a:hover
  cursor: pointer
</style>
