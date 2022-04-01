<template lang="pug">
  #main.main-content.flex-1.py-20(class="md:pb-5")
    .px-4.text-gray-700(class="md:px-8")
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.w-6.h-6(aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor")
          path(d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01")
        div Điểm danh
      .items-center.mt-4.gap-36(class="md:flex")
        h1.py-2
          span Tên lớp: {{ classroom.name }}
        h1.py-2
          span Sĩ số: {{ students.length }}

        v-btn(@click="handleClickRollCall()") {{ addCols ? 'Hủy Điểm danh' : 'Điểm danh'}}

      // Danh sách sinh viên
      .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
        .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-1.py-1.text-center.border.sticky.w-10.l-0 STT
                th.px-1.py-1.text-center.border.border.sticky.w-10.l-0 Mã HS
                th.px-1.py-1.border Họ tên
                th.px-1.py-1.border(v-for="rollCall in rollCalls" :key="rollCall.date")
                  span {{ rollCall.date }}
                th.px-1.py-1.border(v-if="addCols")
                  span {{ moment(new Date()).format('YYYY-MM-DD') }}
                //th.px-1.py-1.border 1/1/2020
                //th.px-1.py-1.border 2/1/2020
                //th.px-1.py-1.border 3/1/2020
                //th.px-1.py-1.border Ghi chú
            tbody.bg-white
              tr.text-gray-700(v-for="(student, index) in studentData" :key="student.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ student.id }}
                td.px-2.py-1.border {{ student.name }}
                td.px-2.py-1.border(v-for="rollCall in rollCalls" :key="rollCall.id")
                  span {{ rollCall.rollCall.find(e => e.student.id === student.id).absentType.type }}
                td.border(v-if="addCols")
                  select.block.bg-white.rounded.w-full.mt-1.form-select(
                    class="focus:outline-none"
                    v-model="student.absentTypeName"
                  )
                    option(v-for="absentType in absentTypes" :key="absentType.id") {{ absentType.type }}
                //td.px-1.py-1.text-sm.border
                //  select.block.bg-white.rounded.w-full.mt-1.form-select(class='focus:outline-none')
                //    option Có mặt
                //    option Vắng
                //td.px-1.py-1.text-sm.border

      v-btn(v-if="addCols" style="margin-left: 77%" @click="onClickSubmit") submit

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'
import moment from 'moment'

interface AbsentType {
  id: number
  type: string
}

interface Master {
  id: number
  name: string
}

interface RollCallDetail {
  id: number
  teacher: Master
  student: Master
  absentType: AbsentType[]
}

interface RollCallType {
  date: string
  rollCall: RollCallDetail
}

interface RollCallCreate {
  date: string
  classroom: number
  teacher: number
  student: number
  absentType?: number
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
    const absentTypes = ref<AbsentType[]>([])
    const rollCalls = ref<RollCallType[]>([])
    const addCols = ref<boolean>(false)
    const studentData = ref<any[]>([])
    const alreadyRollCall = ref(false)
    studentData.value = props.students.map((student: any) => {
      return { ...student, absentTypeName: 'Đúng giờ' }
    })

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.ABSENTTYPE}`),
          api.get(`${endpoints.ROLLCALL}?class_room=${props.classroom.id}`)
        ])

        const [{ data: absentTypeData }, { data: rollCallData }] = data

        absentTypes.value = toCamelCase(absentTypeData)
        rollCalls.value = toCamelCase(rollCallData)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
      addCols.value = false
    }

    const saveRollCallAPI = async (query: RollCallCreate[]) => {
      try {
        await api.post(`${endpoints.ROLLCALL}create_roll_calls`, query)
        await reload()
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const onClickSubmit = () => {
      const query: RollCallCreate[] = []
      studentData.value.forEach((student: any) => {
        query.push({
          date: moment(new Date()).format('YYYY-MM-DD'),
          classroom: props.classroom.id,
          teacher: props.teacher.id,
          student: student.id,
          absentType: absentTypes.value.find((e: AbsentType) => e.type === student.absentTypeName)
            ?.id
        })
      })
      saveRollCallAPI(toSnakeCase(query))
    }

    const handleClickRollCall = () => {
      if (alreadyRollCall.value) $toast.info('Hôm nay đã điểm danh')
      else addCols.value = !addCols.value
    }

    onMounted(async () => {
      await getData()
      alreadyRollCall.value =
        rollCalls.value.map((e: any) => e.date).indexOf(moment(new Date()).format('YYYY-MM-DD')) >
        -1
    })
    return {
      absentTypes,
      rollCalls,
      addCols,
      onClickSubmit,
      studentData,
      alreadyRollCall,
      handleClickRollCall
    }
  }
})

export default RollCall
</script>

<style lang="sass">
select
  color: deeppink
  cursor: pointer
  border-color: #0E5A84
</style>