<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
          path(stroke-linecap='round' stroke-linejoin='round' d='M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z')
        div Quản lí giáo viên
      .mt-4
        .items-center.justify-between(class='md:flex lg:px-10')
          .flex.border-2.border-gray-200.rounded.w-96
            input.px-4.py-2.w-80(type='text' class='focus:outline-none' placeholder='Search...')
            button.px-4.text-white.bg-orange-400.border-l.border-l-orange-400(class='hover:bg-orange-300')
              | Search
          button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(class='hover:bg-green-500 md:mt-0' data-modal-toggle='themgv')
            | + Thêm giáo viên
          #themgv.hidden.overflow-y-auto.overflow-x-hidden.fixed.right-0.left-0.top-4.z-50.justify-center.items-center.h-modal(aria-hidden='true' class='md:h-full md:inset-0')
            .relative.px-4.w-full.max-w-2xl.h-full(class='md:h-auto')
              // Modal content
              .relative.bg-white.rounded-lg.shadow
                // Modal header
                .flex.justify-between.items-start.p-5.rounded-t.border-b(class='dark:border-gray-600')
                  h3.text-xl.font-semibold.text-gray-900(class='lg:text-2xl')
                    | Thêm giáo viên
                  button.text-gray-400.bg-transparent.rounded-lg.text-sm.ml-auto.inline-flex.items-center(type='button' class='hover:bg-gray-200 hover:text-gray-900 p-1.5 dark:hover:bg-gray-600 dark:hover:text-white' data-modal-toggle='themgv')
                    svg.w-5.h-5(fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg')
                      path(fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd')
                // Modal body
                .p-6.space-y-6
                  .mb-4
                    label.block.text-gray-700.text-sm.font-bold.mb-2(for='username')
                      | Tên
                    input#username.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(class='focus:outline-none focus:shadow-outline' type='text' placeholder='Username')
                  .mb-4
                    label.block.text-gray-700.text-sm.font-bold.mb-2(for='username')
                      | Tên
                    input#username.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(class='focus:outline-none focus:shadow-outline' type='text' placeholder='Username')
                  .mb-4
                    label.block.text-gray-700.text-sm.font-bold.mb-2(for='username')
                      | Tên
                    input#username.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(class='focus:outline-none focus:shadow-outline' type='text' placeholder='Username')
                  .mb-4
                    label.block.text-gray-700.text-sm.font-bold.mb-2(for='username')
                      | Tên
                    input#username.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(class='focus:outline-none focus:shadow-outline' type='text' placeholder='Username')
                // Modal footer
                .flex.items-center.p-6.space-x-2.rounded-b.border-t.border-gray-200.justify-center(class='dark:border-gray-600')
                  button.text-white.bg-green-600.font-medium.rounded-lg.text-sm.px-5.text-center(data-modal-toggle='defaultModal' type='button' class='hover:bg-green-500 focus:ring-4 focus:ring-blue-300 py-2.5')
                    | Thêm
        .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
          .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
            table.w-full.whitespace-nowrap.rounded-lg.border
              thead
                tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                  th.px-4.py-3.text-center.border STT
                  th.px-4.py-3.border Mã giáo viên
                  th.px-4.py-3.border Họ tên
                  th.px-4.py-3.border Ngày sinh
                  th.px-4.py-3.border Giới tính
                  th.px-4.py-3.border.text-center Lớp học đang dạy
                  th.px-4.py-3.border.text-center Tùy chọn
              tbody.bg-white
                tr.text-gray-700
                  td.px-4.py-3.border.text-center 1
                  td.px-4.py-3.border B18DCCB423
                  td.px-4.py-3.border Lê Hoàng Nam
                  td.px-4.py-3.text-sm.border 6/4/2000
                  td.px-4.py-3.text-sm.border Nam
                  td.px-4.py-3.text-sm.border
                    .flex.justify-center
                      button.bg-blue-500.text-white.px-4.py-2.rounded.mt-6(class='hover:bg-blue-400 md:mt-0' data-modal-toggle='xem')
                        | Xem
                    #xem.hidden.overflow-y-auto.overflow-x-hidden.fixed.right-0.left-0.top-4.z-50.justify-center.items-center.h-modal(aria-hidden='true' class='md:h-full md:inset-0')
                      .relative.px-4.w-full.max-w-4xl.h-full(class='md:h-auto')
                        // Modal content
                        .relative.bg-white.rounded-lg.shadow
                          // Modal header
                          .flex.justify-between.items-start.p-5.rounded-t.border-b(class='dark:border-gray-600')
                            h3.text-xl.font-semibold.text-gray-900(class='lg:text-2xl')
                              | Môn học đang dạy
                            button.text-gray-400.bg-transparent.rounded-lg.text-sm.ml-auto.inline-flex.items-center(type='button' class='hover:bg-gray-200 hover:text-gray-900 p-1.5 dark:hover:bg-gray-600 dark:hover:text-white' data-modal-toggle='xem')
                              svg.w-5.h-5(fill='currentColor' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg')
                                path(fill-rule='evenodd' d='M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z' clip-rule='evenodd')
                          // Modal body
                          .p-6.space-y-6
                            .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
                              .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
                                table.w-full.whitespace-nowrap.rounded-lg.border
                                  thead
                                    tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                                      th.px-4.py-3.text-center.border
                                        | STT
                                      th.px-4.py-3.border Mã môn học
                                      th.px-4.py-3.border
                                        | Tên môn học
                                      th.px-4.py-3.border
                                        | Ngày bắt đầu
                                      th.px-4.py-3.border Ghi chú
                                  tbody.bg-white
                                    tr.text-gray-700
                                      td.px-4.py-3.border.text-center
                                        | 1
                                      td.px-4.py-3.border B18DCCB423
                                      td.px-4.py-3.border TOán
                                      td.px-4.py-3.text-sm.border
                                        | 6/4/2000
                                      td.px-4.py-3.text-sm.border
                  td.px-4.py-3.text-sm.border
                    .flex.items-center.justify-center.gap-4
                      button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(class='hover:bg-green-500 md:mt-0' data-modal-toggle='themgv')
                        | Sửa
                      button.bg-red-500.text-white.px-4.py-2.rounded.mt-6(class='hover:bg-red-400 md:mt-0')
                        | Xóa

</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const TeacherManagement = defineComponent({
  setup() {
    return {}
  }
})

export default TeacherManagement
</script>

<style lang="sass"></style>
