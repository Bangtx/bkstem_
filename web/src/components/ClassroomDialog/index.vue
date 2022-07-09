<template lang="pug">
  div
    v-dialog(:value="value" max-width="400" persistent)
      v-card
        v-card-title.text-h5.title-color.lighten-2
          span {{ title.toUpperCase() }}
          v-spacer
          v-btn(icon @click="$emit('on-close')")
            v-icon mdi-close

        v-card-text
          v-text-field.p-0(:label="'tên'" v-model="classroom.name")
          v-select.p-0(
            :label="'giáo viên'"
            :items="selectTeacher"
            v-model="selectedTeacher"
          )
          v-text-field.p-0(:label="'phòng'" v-model="classroom.room")
          v-select.p-0(
            multiple
            :label="'thời gian'"
            :items="selectClassTime"
            v-model="selectedClassTimes"
          )
          v-select.p-0(
            multiple
            :label="'trợ giảng'"
            :items="teachers"
            item-text="name"
            item-value="id"
            v-model="assistantTeachers"
          )

        v-card-actions
          v-btn.relative-btn(
            :large="!$vuetify.breakpoint.xsOnly"
            block
            @click="onSave()"
          )
            span Lưu
    class-time-dialog(
      :value="isOpenClassTimeDialog"
      @reload="reload()"
      @on-close="isOpenClassTimeDialog=false"
    )

</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from '@vue/composition-api'
import moment from 'moment'
import { api } from 'plugins'
import { endpoints, toCamelCase, toSnakeCase } from 'utils'
import ClassTimeDialog from '@/components/ClassTimeDialog/index.vue'

interface Student {
  id: number
  name: string
  dateOfBirth: string
  gender: string
}

interface Teacher {
  id: number
  name: string
  dateOfBirth: string
  gender: string
}

const ClassroomDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    mode: {
      type: String,
      required: false,
      default: 'edit'
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  components: {
    ClassTimeDialog
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const modal = ref(false)
    const password = ref('')
    const date = moment(new Date()).format('YYYY-MM-DD')
    const students = ref<Student[]>([])
    const teachers = ref<Teacher[]>([])
    const selectTeacher = ref<any[]>([])
    const selectClassTime = ref<any[]>([])
    const classTimes = ref<any[]>([])
    const isOpenClassTimeDialog = ref(false)
    const selectedTeacher = ref('')
    const selectedClassTimes = ref<string[]>([])
    const assistantTeachers = ref<number[]>([])

    const onSave = async () => {
      const selectedClassTimesObject = classTimes.value
        .filter((classTime: any) => {
          return (
            selectedClassTimes.value.indexOf(
              `[${classTime.dateOfWeek.name}] ${classTime.startTime} -> ${classTime.stopTime}`
            ) > -1
          )
        })
        .map((e: any) => e.id)
      const body = {
        id: props.classroom.id,
        name: props.classroom.name,
        room: props.classroom.room,
        classTimeIds: selectedClassTimesObject,
        startDate: props.classroom.startDate,
        teacher: teachers.value.find((e: any) => `[${e.id}] ${e.name}` === selectedTeacher.value)
          ?.id,
        studentIds: props.classroom.students.map((e: any) => e.id),
        assistantTeacher: assistantTeachers.value
      }

      try {
        if (props.mode === 'add') {
          await api.post(`${endpoints.CLASSROOM}`, toSnakeCase(body))
        } else {
          await api.put(`${endpoints.CLASSROOM}${props.classroom.id}`, toSnakeCase(body))
        }
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch {
        $toast.error('Save data failed')
      }
    }

    const getData = async () => {
      try {
        const data = await Promise.all([
          api.get(`${endpoints.TEACHER}`),
          api.get(`${endpoints.STUDENT}`),
          api.get(`${endpoints.CLASS_TIME}`)
        ])
        const [{ data: teacherData }, { data: studentData }, { data: classTimeData }] = data
        teachers.value = toCamelCase(teacherData)
        students.value = toCamelCase(studentData)
        classTimes.value = toCamelCase(classTimeData)

        selectTeacher.value = teachers.value.map((teacher: Teacher) => {
          return `[${teacher.id}] ${teacher.name}`
        })

        selectClassTime.value = ['Thêm mới'].concat(
          classTimes.value.map((classTime: any) => {
            return `[${classTime.dateOfWeek.name}] ${classTime.startTime} -> ${classTime.stopTime}`
          })
        )
      } catch {
        $toast.error('Get data failed')
      }
    }

    const reload = async () => {
      await getData()
    }

    onMounted(async () => {
      await getData()
    })

    watch(
      () => props.value,
      () => {
        if (props.value) {
          if (props.mode === 'edit') {
            const teacher: any = teachers.value.find(
              (e: any) => e.id === props.classroom.teacher.id
            )
            selectedTeacher.value = `[${teacher.id}] ${teacher.name}`

            // console.log(classTimes.value, props.classroom)
            selectedClassTimes.value = classTimes.value
              .filter((classTime: any) => {
                return props.classroom.classTimes.map((e: any) => e.id).indexOf(classTime.id) > -1
              })
              .map(
                (classTime: any) =>
                  `[${classTime.dateOfWeek.name}] ${classTime.startTime} -> ${classTime.stopTime}`
              )
            // console.log(selectedClassTimes.value, 'selectedClassTimes')

            assistantTeachers.value = props.classroom.assistantTeachers
            // console.log(assistantTeachers.value)
          }
        }
      }
    )

    watch(
      () => selectedClassTimes.value,
      () => {
        if (selectedClassTimes.value.indexOf('Thêm mới') > -1) {
          isOpenClassTimeDialog.value = true
          selectedClassTimes.value.splice(selectedClassTimes.value.indexOf('Thêm mới'))
        }
      }
    )

    return {
      modal,
      date,
      onSave,
      password,
      students,
      teachers,
      selectTeacher,
      selectClassTime,
      isOpenClassTimeDialog,
      reload,
      selectedTeacher,
      selectedClassTimes,
      assistantTeachers
    }
  }
})

export default ClassroomDialog
</script>

<style lang="sass">
.v-picker__title
  background-color: beige !important
  color: #343f4b !important
.v-date-picker-table .v-btn.v-btn--active
  background-color: beige !important
  color: #343f4b !important
</style>
