<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-5.w-5(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
          path(stroke-linecap='round' stroke-linejoin='round' d='M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z')
          path(stroke-linecap='round' stroke-linejoin='round' d='M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z')
        div Điểm số
      .items-center.mt-4.gap-36(class='md:flex')
        h1.py-2
          | Tên lớp:
          span Toán cao cấp
        h1.py-2
          | Sĩ số:
          span 32
        v-btn(
          v-if="member.typeMember === 'teacher'"
          @click="handleClickAddCol()"
        ) {{ addCols ? 'Hủy nhập' : 'Nhập điểm'}}
      // Danh sách sinh viên
      .rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(
           v-if="member.typeMember === 'teacher'"
          style='max-height: 600px; max-width: 1550px;'
        )
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-2.py-1.text-center.border.sticky.w-44.l-0 STT
                th.px-2.py-1.border.w-44 Mã học viên
                th.px-2.py-1.border.w-44 Họ tên
                th.px-2.py-1.border.w-44(
                  v-for="(scoreData, index) in scoreDatas" :key="scoreData.date"
                  @click="editDate(scoreData.date, index)"
                )
                  span {{ scoreData.date }}
                th.px-2.py-1.border.text-click-able(v-if="addCols" @click="editDate(dateAddScore)")
                  span {{ dateAddScore }}
                //th.px-2.py-1.border Trung bình
                th.px-2.py-1.border Ghi chú
            tbody.bg-white
              tr.text-gray-700(v-for="(student, index) in studentDatas" :key="student.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ student.id }}
                td.px-2.py-1.border {{ student.name }}
                td.px-2.py-1.border(v-for="scoreData in scoreDatas" :key="scoreData.date")
                  //span.text-click-able {{ scoreData.data }}
                  span L:{{ scoreData.data.find(e => e.student.id === student.id).score.listening || '_' }}
                  span S:{{ scoreData.data.find(e => e.student.id === student.id).score.specking || '_' }}
                  span R:{{ scoreData.data.find(e => e.student.id === student.id).score.reading || '_' }}
                  span W:{{ scoreData.data.find(e => e.student.id === student.id).score.writing || '_' }}
                td.px-2.py-1.text-sm.border.text-center(v-if="addCols")
                  v-text-field.pa-0.ma-0(
                    label="Nghe"
                    type="number" v-model="student.score.listening"
                  )
                  v-text-field.pa-0.ma-0(
                    label="Nói"
                    type="number" v-model="student.score.specking"
                  )
                  v-text-field.pa-0.ma-0(
                    label="Đọc"
                    type="number" v-model="student.score.reading"
                  )
                  v-text-field.pa-0.ma-0(
                    label="Viết"
                    type="number" v-model="student.score.writing"
                  )

                //td.px-2.py-1.text-sm.border.text-center
                //  span {{ student.average ? student.average.toFixed(2) : '' }}
                td.px-2.py-1.text-sm.border

        .w-full.overflow-auto.rounded-lg(
           v-if="member.typeMember === 'student'"
          style='max-height: 600px; max-width: 1550px;'
        )
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-2.py-1.border.w-44 Mã học viên
                th.px-2.py-1.border.w-44 Họ tên
                th.px-2.py-1.border.w-44 Ngày
                th.px-2.py-1.border.w-44 Điểm
            tbody.bg-white
              tr.text-gray-700(v-for="scoreData in scoreDatas")
                td.px-2.py-1.border {{ member.id }}
                td.px-2.py-1.border {{ member.name }}
                td.px-2.py-1.border {{ scoreData.data.find(e => e.student.id === member.id).date }}
                td.px-2.py-1.border
                  span L:{{ scoreData.data.find(e => e.student.id === member.id).score.listening || '_' }}
                  span S:{{ scoreData.data.find(e => e.student.id === member.id).score.specking || '_' }}
                  span R:{{ scoreData.data.find(e => e.student.id === member.id).score.reading || '_' }}
                  span W:{{ scoreData.data.find(e => e.student.id === member.id).score.writing || '_' }}
                //td.px-2.py-1.border {{ scoreData.data.find(e => e.student.id === member.id).score.join(', ') }}

      v-btn(v-if="addCols" style="margin-left: 77%" @click="onSave()") Lưu

      .rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(
           v-if="member.typeMember === 'teacher'"
          style='max-height: 600px; max-width: 1550px;'
        )
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-2.py-1.text-center.border.sticky.w-44.l-0 STT
                th.px-2.py-1.border.w-44 Họ tên
                th.px-2.py-1.border.w-44(v-for="unit in units" :key="unit.id")
                  span {{ unit.title }}

            tbody.bg-white
              tr.text-gray-700(v-for="(scoreHomeWork, index) in scoreHomeWorks" :key="scoreHomeWork.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ scoreHomeWork.name }}
                  //span {{ scoreHomeWork }}
                th.px-2.py-1.border.w-44(v-for="(unit, indexUnit) in scoreHomeWork.result")
                  span {{ unit[units[indexUnit].id] }}

        .w-full.overflow-auto.rounded-lg(
           v-if="member.typeMember === 'student'"
          style='max-height: 600px; max-width: 1550px;'
        )
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-2.py-1.border.w-44 Mã học viên
                th.px-2.py-1.border.w-44 Họ tên
                th.px-2.py-1.border.w-44(v-for="unit in units" :key="unit.id")
                  span {{ unit.title }}
            tbody.bg-white
              td.px-2.py-1.border {{ member.id }}
              td.px-2.py-1.border {{ member.name }}
              th.px-2.py-1.border.w-44(v-for="(unit, indexUnit) in scoreHomeWorks.find(e => e.id === member.id).result")
                span {{ unit[units[indexUnit].id] }}

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

</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'
import moment from 'moment'
import jwtDecode from 'jwt-decode'

interface StudentData {
  id: number
  name: string
  dateOfBirth: string
  gender: string
  score: any
  average?: number
}

interface Master {
  id: number
  name: string
}

interface ScoreData {
  classroom: Master
  teacher: Master
  student: Master
  score: any
}

interface ScoreType {
  date: string
  data: ScoreData[]
}

const Score = defineComponent({
  props: {
    classroom: {
      type: Object,
      required: true
    },
    students: {
      type: Array,
      required: true
    },
    units: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const addCols = ref(false)
    const studentDatas = ref<StudentData[]>([])
    studentDatas.value = JSON.parse(JSON.stringify(props.students))
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const dateAddScore = ref(moment(new Date()).format('YYYY-MM-DD'))
    const scoreDatas = ref<ScoreType[]>([])
    const scoreHomeWorks = ref<any[]>([])
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))
    const currentIndexDate = ref(0)

    const handleClickAddCol = () => {
      studentDatas.value = props.students.map((studentData: any) => {
        return {
          ...studentData,
          score: { specking: null, reading: null, writing: null, listening: null }
        }
      })
      addCols.value = !addCols.value
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.SCORE}?class_room=${props.classroom.id}`),
          api.get(
            `${endpoints.HOME_WORK_STUDENT}check_rate_corrects?classroom_id=${props.classroom.id}`
          )
        ])
        const [{ data: scoreData }, { data: homeworkData }] = data
        scoreHomeWorks.value = toCamelCase(homeworkData)
        // const { data } = await api.get(`${endpoints.SCORE}?class_room=${props.classroom.id}`)
        scoreDatas.value = toCamelCase(scoreData)
      } catch {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
    }

    const addScoreAPI = async () => {
      const params = ref<any[]>([])
      studentDatas.value.forEach((studentData: StudentData) => {
        params.value.push({
          date: dateAddScore.value,
          classroom: props.classroom.id,
          student: studentData.id,
          teacher: member.id,
          score: {
            specking: studentData.score.specking ? Number(studentData.score.specking) : null,
            reading: studentData.score.reading ? Number(studentData.score.reading) : null,
            writing: studentData.score.writing ? Number(studentData.score.writing) : null,
            listening: studentData.score.listening ? Number(studentData.score.listening) : null
          }
        })
      })
      try {
        await api.post(`${endpoints.SCORE}`, params.value)
        $toast.success('Save data successful')
      } catch {
        $toast.error('Add data failed')
      }
      await reload()
    }

    const onSave = async () => {
      const validate = studentDatas.value.find((e: StudentData) => Number(e.score) > 10)
      if (validate) $toast.error('Điểm chỉ được phép từ 0 -> 10')
      else await addScoreAPI()
      addCols.value = false
    }

    const editDate = (dateData: string, indexDate?: number) => {
      date.value = dateData
      if (indexDate) currentIndexDate.value = indexDate
      modal.value = true
    }

    const savaDate = () => {
      if (addCols.value) dateAddScore.value = date.value
      else scoreDatas.value[currentIndexDate.value].date = date.value
    }

    onMounted(async () => {
      await getData()
    })

    return {
      addCols,
      studentDatas,
      handleClickAddCol,
      onSave,
      dateAddScore,
      scoreDatas,
      member,
      scoreHomeWorks,
      editDate,
      modal,
      date,
      savaDate
    }
  }
})

export default Score
</script>

<style lang="sass">
.v-text-field__details
  display: none !important
.v-text-field__slot input
  margin: 2px !important
  padding: 0 !important
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
</style>
