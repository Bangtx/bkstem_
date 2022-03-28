<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      h1.flex.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-6.w-6.mr-1(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
          path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
        div Trang chủ
      .items-center.mt-4.gap-36(class='md:flex')
        h1.py-2
          | Tên lớp:
          span {{ classroom.name }}
        h1.py-2
          | Sĩ số:
          span {{ students.length }}
      h1.py-2
        | Giáo viên chủ nhiệm:
        span {{ teacher.name }}
      h1.py-2.flex.gap-2.items-center
        div Danh sách sinh viên
      // Danh sách sinh viên
      .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-4.py-3.text-center.border STT
                th.px-4.py-3.border Mã học viên
                th.px-4.py-3.border Họ tên
                th.px-4.py-3.border Ngày sinh
                th.px-4.py-3.border Giới tính
                th.px-4.py-3.border Ghi chú
            tbody.bg-white(v-for="(student, index) in students" :key="student.id")
              tr.text-gray-700
                td.px-4.py-3.border.text-center {{ index }}
                td.px-4.py-3.border {{ student.id }}
                td.px-4.py-3.border {{ student.name }}
                td.px-4.py-3.text-sm.border {{ student.dateOfBirth }}
                td.px-4.py-3.text-sm.border {{ student.gender }}
                td.px-4.py-3.text-sm.border
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

const ClassHome = defineComponent({
  props: {
    classroom: {
      type: Object,
      required: true
    },
    students: {
      type: Array,
      required: true
    },
    teacher: {
      type: Object,
      required: true
    }
  },
  setup() {
    return {}
  }
})

export default ClassHome
</script>
