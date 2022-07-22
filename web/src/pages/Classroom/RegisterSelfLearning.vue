<template lang="pug">
  div
    #main.main-content.flex-1.py-20(class='md:pb-5')
      .px-4.text-gray-700(class='md:px-8')
        .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
          svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
          div Trang chủ
          svg.h-5.w-5(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M9 5l7 7-7 7')
          svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
            path(stroke-linecap='round' stroke-linejoin='round' d='M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z')
          div Giao bài tập
        .flex.justify-between.items-center
          .text-lg Danh sách đã đăng kí
          button.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
            v-if="member.typeMember === 'student'"
            @click="openRegisterSelfLearningDialog()"
            class='hover:bg-orange-300 focus:outline-none'
          )
            svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
              path(stroke-linecap='round' stroke-linejoin='round' d='M12 6v6m0 0v6m0-6h6m-6 0H6')
            span.text-base Đăng kí
        .mt-2(class='md:px-4')

    register-self-learning-dialog(
      :value="isOpenRegisterSelfLearningDialog"
      :data="dataRegisterProps"
      @on-close="isOpenRegisterSelfLearningDialog = false"
    )

    .rounded-lg.overflow-auto.shadow-xs.mt-4(class="lg:px-10")
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
            tr.text-gray-700(v-for="(selfLearning, index) in selfLearnings" :key="index")
              td.px-2.py-1.border.text-center {{ index + 1 }}
              td.px-2.py-1.border {{ selfLearning.date }}
              td.px-2.py-1.border {{ member.name }}
              td.px-2.py-1.border {{ selfLearning.absentType ? selfLearning.absentType : '' }}

      .w-full.overflow-auto.rounded-lg(style="max-height: 600px; max-width: 1550px;")
        table.w-full.whitespace-nowrap.rounded-lg.border.mt-4(
          v-if="member.typeMember === 'teacher'"
          v-for="student in studentData"
        )
          thead
            tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
              th.px-1.py-1.border STT
              th.px-1.py-1.border Ngày
              th.px-1.py-1.border Tên
              th.px-1.py-1.border Điểm danh
          tbody.bg-white
            tr.text-gray-700(v-for="(selfL, index) in student.data" :key="index")
              td.px-2.py-1.border.text-center {{ index + 1 }}
              td.px-2.py-1.border {{ selfL.date }}
              td.px-2.py-1.border {{ student.student.name }}
              td.px-2.py-1.border(@dblclick="onEditRollCall(selfL.id, student.student.id, selfL.date)") {{ selfL.absentType }}

    edit-roll-call-dialog(
      :value="isShowEdit"
      :data="rollCallProps"
      :absent-types="absentTypes"
      :is-self-learning="true"
      @on-close="isShowEdit = false"
      @reload="getData(), getAbsentType()"
    )

</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'
import { RegisterSelfLearningDialog, EditRollCallDialog } from 'components'
import jwtDecode from 'jwt-decode'

const RegisterSelfLearning = defineComponent({
  props: {
    classroom: {
      type: Object,
      required: true
    }
  },
  components: {
    RegisterSelfLearningDialog,
    EditRollCallDialog
  },
  setup(props, { root }) {
    const { $toast } = root
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const isOpenRegisterSelfLearningDialog = ref(false)
    const selfLearnings = ref([])
    const selfLearningAllStudents = ref([])
    const dataRegisterProps = ref({})
    const studentData = ref<any>([])
    const isShowEdit = ref(false)
    const absentTypes = ref<any>([])
    const rollCallProps = ref<any>({})

    const onEditRollCall = (id: number, studentId: any, rollCallDate: any) => {
      // console.log(studentId, rollCallDate)
      rollCallProps.value = {
        id,
        student: studentId,
        date: rollCallDate,
        absentType: null,
        classroom: props.classroom.id
      }
      isShowEdit.value = true
    }

    const openRegisterSelfLearningDialog = () => {
      isOpenRegisterSelfLearningDialog.value = true
      dataRegisterProps.value = {
        classroom: props.classroom.id,
        student: member.id,
        dates: selfLearnings.value.map((e: any) => e.date)
      }
    }

    const groupStudent = () => {
      let students = selfLearningAllStudents.value.map((e: any) => e.student.id)
      students = [...new Set(students)]
      studentData.value = []
      students.forEach((student: any) => {
        const stu: any = selfLearningAllStudents.value.filter((e: any) => e.student.id === student)
        studentData.value.push({
          student: stu[0].student,
          data: stu
        })
      })
    }

    const getData = async () => {
      try {
        if (member.typeMember === 'teacher') {
          const { data } = await api.get(
            `${endpoints.SELF_LEARNING}?classroom=${props.classroom.id}`
          )
          selfLearningAllStudents.value = toCamelCase(data)
          groupStudent()
        } else {
          const { data } = await api.get(
            `${endpoints.SELF_LEARNING}?classroom=${props.classroom.id}&student=${member.id}`
          )
          selfLearnings.value = toCamelCase(data)
        }
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const getAbsentType = async () => {
      try {
        const { data } = await api.get(`${endpoints.ABSENTTYPE}`)
        absentTypes.value = toCamelCase(data)
      } catch {
        $toast.error('Get data failed')
      }
    }

    onMounted(async () => {
      await getData()
      await getAbsentType()
    })

    return {
      member,
      openRegisterSelfLearningDialog,
      isOpenRegisterSelfLearningDialog,
      selfLearnings,
      dataRegisterProps,
      studentData,
      selfLearningAllStudents,
      onEditRollCall,
      isShowEdit,
      absentTypes,
      rollCallProps,
      getData,
      getAbsentType
    }
  }
})

export default RegisterSelfLearning
</script>

<style lang="sass"></style>
