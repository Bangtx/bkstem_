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
        v-btn(@click="handleClickAddCol()") {{ addCols ? 'Hủy nhập' : 'Nhập điểm'}}
      // Danh sách sinh viên
      .rounded-lg.overflow-auto.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(style='max-height: 600px; max-width: 1550px;')
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-2.py-1.text-center.border.sticky.w-44.l-0 STT
                th.px-2.py-1.border.w-44 Mã học viên
                th.px-2.py-1.border.w-44 Họ tên
                th.px-2.py-1.border.w-44(v-for="scoreData in scoreDatas" :key="scoreData.date")
                  span {{ scoreData.date }}
                th.px-2.py-1.border(v-if="addCols")
                  span {{ dateAddScore }}
                th.px-2.py-1.border Trung bình
                th.px-2.py-1.border Ghi chú
            tbody.bg-white
              tr.text-gray-700(v-for="(student, index) in studentDatas" :key="student.id")
                td.px-2.py-1.border.text-center {{ index + 1 }}
                td.px-2.py-1.border {{ student.id }}
                td.px-2.py-1.border {{ student.name }}
                td.px-2.py-1.border(v-for="scoreData in scoreDatas" :key="scoreData.date")
                  span {{ scoreData.data.find(e => e.student.id === student.id).score.join(', ') }}
                td.px-2.py-1.text-sm.border.text-center(v-if="addCols")
                  v-text-field.pa-0.ma-0(
                    type="number" v-model="student.score"
                  )
                td.px-2.py-1.text-sm.border.text-center 9
                td.px-2.py-1.text-sm.border
      v-btn(v-if="addCols" style="margin-left: 77%" @click="onSave()") Lưu

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
  score: number | null | string
}

interface Master {
  id: number
  name: string
}

interface ScoreData {
  classroom: Master
  teacher: Master
  student: Master
  score: number
}

interface ScoreType {
  date: string
  data: ScoreData
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
    }
  },
  setup(props, { root }) {
    const { $toast } = root
    const addCols = ref(false)
    const studentDatas = ref<StudentData[]>([])
    studentDatas.value = JSON.parse(JSON.stringify(props.students))
    const teacher: any = jwtDecode(String(localStorage.getItem('token')))
    console.log(teacher)
    const dateAddScore = ref(moment(new Date()).format('YYYY-MM-DD'))
    const scoreDatas = ref<ScoreType[]>([])

    const handleClickAddCol = () => {
      studentDatas.value = props.students.map((studentData: any) => {
        return { ...studentData, score: null }
      })
      addCols.value = !addCols.value
    }

    const getData = async () => {
      try {
        const { data } = await api.get(`${endpoints.SCORE}?class_room=${props.classroom.id}`)
        scoreDatas.value = toCamelCase(data)
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
          teacher: teacher.id,
          score: studentData.score
        })
      })
      try {
        await api.post(`${endpoints.SCORE}`, params.value)
        await reload()
        $toast.success('Save data successful')
      } catch {
        $toast.error('Add data failed')
      }
    }

    const onSave = async () => {
      const validate = studentDatas.value.find((e: StudentData) => Number(e.score) > 10)
      if (validate) $toast.error('Điểm chỉ được phép từ 0 -> 10')
      else await addScoreAPI()
      addCols.value = false
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
      scoreDatas
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
</style>
