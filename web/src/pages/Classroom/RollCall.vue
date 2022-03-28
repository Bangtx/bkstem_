<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.w-6.h-6(aria-hidden='true' fill='none' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' viewBox='0 0 24 24' stroke='currentColor')
          path(d='M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01')
        div Điểm danh
      .items-center.mt-4.gap-36(class='md:flex')
        h1.py-2
          span Tên lớp: {{ classroom.name }}
        h1.py-2
          span Sĩ số: {{ students.length }}

        v-btn Add date

      // Danh sách sinh viên
      .rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(style='max-height: 600px; max-width: 1550px;')
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-4.py-3.text-center.border.sticky.w-44.l-0 STT
                th.px-4.py-3.border.w-44 Mã học viên
                th.px-4.py-3.border.w-44 Họ tên
                //th.px-4.py-3.border 1/1/2020
                //th.px-4.py-3.border 2/1/2020
                //th.px-4.py-3.border 3/1/2020
                //th.px-4.py-3.border Ghi chú
            tbody.bg-white
              tr.text-gray-700(v-for="student in students" :key="student.id")
                td.px-4.py-3.border.text-center 1
                td.px-4.py-3.border {{ student.id }}
                td.px-4.py-3.border {{ student.name }}
                //td.px-4.py-3.text-sm.border
                //  select.block.bg-white.rounded.w-full.mt-1.form-select(class='focus:outline-none')
                //    option Có mặt
                //    option Vắng
                //td.px-4.py-3.text-sm.border
                //  select.block.bg-white.rounded.w-full.mt-1.form-select(class='focus:outline-none')
                //    option Có mặt
                //    option Vắng
                //td.px-4.py-3.text-sm.border
                //  select.block.bg-white.rounded.w-full.mt-1.form-select(class='focus:outline-none')
                //    option Có mặt
                //    option Vắng
                //td.px-4.py-3.text-sm.border

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'

interface AbsentType {
  id: number
  type: string
}

interface Master {
  id: number
  name: string
}

interface RollCallType {
  id: number
  date: string
  classRoom: Master
  teacher: Master
  student: Master
  absentType: AbsentType
}

const RollCall = defineComponent({
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
  setup(props, { root }) {
    const { $toast } = root
    const absentType = ref<AbsentType[]>([])
    const rollCalls = ref<RollCallType[]>([])
    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.ABSENTTYPE}`),
          api.get(`${endpoints.ROLLCALL}`)
        ])

        const [{ data: absentTypeData }, { data: rollCallData }] = data

        absentType.value = toCamelCase(absentTypeData)
        rollCalls.value = toCamelCase(rollCallData)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
    })
    return {
      absentType
    }
  }
})

export default RollCall
</script>

<style lang="sass"></style>
