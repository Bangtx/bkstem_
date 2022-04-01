<template lang="pug">
  #main.main-content.flex-1.py-20(class="md:pb-5")
    .px-4.text-gray-700(class="md:px-8")
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-5.w-5(xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2")
          path(stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z")
        div Lịch học
      .items-center.mt-4.gap-36(class="md:flex")
        h1.py-2
          | Tên lớp:
          span Toán cao cấp
        h1.py-2
          | Sĩ số:
          span 32
      div
        .gap-4.mt-4(class="md:flex")
          div
            h2.pb-2 Tuần
            .mb-3.w-64(class="md:w-96")
              select.form-select.appearance-none.block.w-full.px-3.text-base.font-normal.text-gray-700.bg-white.bg-clip-padding.bg-no-repeat.border.border-solid.border-gray-300.rounded.transition.ease-in-out.m-0(class="py-1.5 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" aria-label="Default select example")
                option(selected="") 1 ( từ 1/1/2021 - 7/1/2021)
                option 2 ( từ 1/1/2021 - 7/1/2021)
                option 3 ( từ 1/1/2021 - 7/1/2021)
                option 4 ( từ 1/1/2021 - 7/1/2021)
          div(class="md:mt-8")
            button.bg-orange-500.text-white.px-4.rounded(class="py-1.5 hover:bg-orange-400") Xem
        .mt-8
          h1 Lịch học
          .grid.gap-6.mb-8.mt-2(class="md:grid-cols-2 xl:grid-cols-3")
            // Card
            .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
              .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
                svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
                  path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
              div
                p.mb-2.text-sm.font-medium.text-gray-600
                  | Thứ 2
                p.text-lg.text-gray-500
                  | 17h00p - 19h00p
                p.text-lg.text-gray-500
                  | Địa điểm: phòng 701 - A2
            // Card
            .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
              .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
                svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
                  path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
              div
                p.mb-2.text-sm.font-medium.text-gray-600
                  | Thứ 2
                p.text-lg.text-gray-500
                  | 17h00p - 19h00p
                p.text-lg.text-gray-500
                  | Địa điểm: phòng 701 - A2
            // Card
            .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
              .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
                svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
                  path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
              div
                p.mb-2.text-sm.font-medium.text-gray-600
                  | Thứ 2
                p.text-lg.text-gray-500
                  | 17h00p - 19h00p
                p.text-lg.text-gray-500
                  | Địa điểm: phòng 701 - A2
            // Card
            .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
              .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
                svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
                  path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
              div
                p.mb-2.text-sm.font-medium.text-gray-600
                  | Thứ 2
                p.text-lg.text-gray-500
                  | 17h00p - 19h00p
                p.text-lg.text-gray-500
                  | Địa điểm: phòng 701 - A2
            // Card
            .flex.items-center.p-4.bg-white.rounded-lg.shadow-xs
              .p-3.mr-4.text-green-500.bg-green-100.rounded-full(class="dark:text-green-100 dark:bg-green-500")
                svg.w-5.h-5(fill="currentColor" viewBox="0 0 20 20")
                  path(fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd")
              div
                p.mb-2.text-sm.font-medium.text-gray-600
                  | Thứ 2
                p.text-lg.text-gray-500
                  | 17h00p - 19h00p
                p.text-lg.text-gray-500
                  | Địa điểm: phòng 701 - A2

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const Schedule = defineComponent({
  setup() {
    return {}
  }
})

export default Schedule
</script>

<style lang="sass"></style>
