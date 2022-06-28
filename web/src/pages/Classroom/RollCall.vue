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

        v-btn(
          v-if="member.typeMember === 'teacher'"
          @click="handleClickRollCall()"
        ) {{ addCols ? 'Hủy Điểm danh' : 'Điểm danh'}}

      .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
        .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
          table.w-full.whitespace-nowrap.rounded-lg.border(
            v-if="member.typeMember === 'teacher'"
          )
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-1.py-1.text-center.border.sticky.w-10.l-0 STT
                th.px-1.py-1.text-center.border.border.sticky.w-10.l-0 Mã HS
                th.px-1.py-1.border Họ tên
                th.px-1.py-1.border(v-for="rollCall in rollCalls" :key="rollCall.date")
                  span {{ rollCall.date }}
                th.px-1.py-1.border(v-if="addCols" @click="editDate(dateAddScore)")
                  span {{ dateAddScore }}

            tbody.bg-white
              tr.text-gray-700(v-for="(student, index) in studentData" :key="student.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ student.id }}
                td.px-2.py-1.border {{ student.name }}
                td.px-2.py-1.border(
                  v-for="rollCall in rollCalls" :key="rollCall.id"
                  @dblclick="onEditRollCall(student.id, rollCall.date)"
                )
                  span {{ rollCall.rollCall.find(e => e.student.id === student.id) ? rollCall.rollCall.find(e => e.student.id === student.id).absentType.type : null}}
                td.border(v-if="addCols")
                  select.block.bg-white.rounded.w-full.mt-1.form-select(
                    class="focus:outline-none"
                    v-model="student.absentTypeName"
                  )
                    option(v-for="absentType in absentTypes" :key="absentType.id") {{ absentType.type }}

        .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
          table.w-full.whitespace-nowrap.rounded-lg.border(
            v-if="member.typeMember === 'student'"
          )
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-1.py-1.border STT
                th.px-1.py-1.border Ngày
                th.px-1.py-1.border Tên
                th.px-1.py-1.border Điểm danh
            tbody.bg-white
              tr.text-gray-700(v-for="(roll, index) in rollCalls" :key="roll.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ roll.date }}
                td.px-2.py-1.border {{ member.name }}
                td.px-2.py-1.border {{ roll.rollCall.find(e => e.student.id === member.id).absentType.type }}

      v-btn(v-if="addCols" style="margin-left: 77%" @click="onClickSubmit") submit

    v-dialog.title-color(
        ref="dialog"
        persistent
        max-width="400"
        :return-value.sync="date"
        v-model="modal"
      )
        v-date-picker(full-width scrollable color="rough_black" header-color="rough_black" v-model="date")
          v-spacer
          v-btn(text color="light_red" @click="modal = false")
            span Cancel
          v-btn(text color="rough_black" @click="$refs.dialog.save(date), savaDate()")
            span Ok

    edit-roll-call-dialog(
      :value="isShowEdit"
      :data="rollCallProps"
      :absent-types="absentTypes"
      @on-close="isShowEdit = false"
      @reload="getData"
    )

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'
import moment from 'moment'
import { EditRollCallDialog } from 'components'
import jwtDecode from 'jwt-decode'

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
  components: {
    EditRollCallDialog
  },
  setup(props, { root }) {
    const { $toast } = root
    const absentTypes = ref<AbsentType[]>([])
    const rollCalls = ref<RollCallType[]>([])
    const addCols = ref<boolean>(false)
    const studentData = ref<any[]>([])
    const alreadyRollCall = ref(false)
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))
    const currentIndexDate = ref(0)
    const dateAddScore = ref(moment(new Date()).format('YYYY-MM-DD'))
    const isShowEdit = ref(false)
    const rollCallProps = ref({
      student: null,
      teacher: null,
      date: null,
      absentType: null,
      classroom: null
    })

    studentData.value = props.students.map((student: any) => {
      return { ...student, absentTypeName: 'Đúng giờ' }
    })

    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))

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

    const onEditRollCall = (studentId: any, rollCallDate: any) => {
      // console.log(studentId, rollCallDate)
      rollCallProps.value = {
        student: studentId,
        teacher: props.teacher.id,
        date: rollCallDate,
        absentType: null,
        classroom: props.classroom.id
      }
      isShowEdit.value = true
    }

    const reload = async () => {
      await getData()
      addCols.value = false
    }

    const saveRollCallAPI = async (query: RollCallCreate[]) => {
      try {
        await api.post(`${endpoints.ROLLCALL}create_roll_calls`, query)
        await reload()
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    const onClickSubmit = () => {
      const query: RollCallCreate[] = []
      studentData.value.forEach((student: any) => {
        query.push({
          date: dateAddScore.value,
          classroom: props.classroom.id,
          teacher: props.teacher.id,
          student: student.id,
          absentType: absentTypes.value.find((e: AbsentType) => e.type === student.absentTypeName)
            ?.id
        })
      })
      saveRollCallAPI(toSnakeCase(query))
    }

    const savaDate = () => {
      dateAddScore.value = date.value
    }

    const editDate = (dateData: string, indexDate?: number) => {
      date.value = dateData
      if (indexDate) currentIndexDate.value = indexDate
      modal.value = true
    }

    const handleClickRollCall = () => {
      // if (alreadyRollCall.value) $toast.info('Hôm nay đã điểm danh')
      // else addCols.value = !addCols.value
      addCols.value = !addCols.value
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
      handleClickRollCall,
      member,
      modal,
      date,
      savaDate,
      dateAddScore,
      editDate,
      onEditRollCall,
      isShowEdit,
      rollCallProps,
      getData
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
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
</style>
