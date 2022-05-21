<template lang="pug">
  #main.main-content.flex-1.py-20(class='md:pb-5')
    .px-4.text-gray-700(class='md:px-8')
      .flex.gap-2.items-center.pb-2.text-xl.font-semibold.text-gray-600.mt-8
        svg.h-6.w-6(xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor' stroke-width='2')
          path(stroke-linecap='round' stroke-linejoin='round' d='M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z')
        span Quản lí {{ title }}
      .mt-4
        .items-center.justify-between(class='md:flex lg:px-10')
          .flex.border-2.border-gray-200.rounded.w-96
            input.px-4.py-2.w-80(type='text' class='focus:outline-none' placeholder='Search...')
            button.px-4.text-white.bg-orange-400.border-l.border-l-orange-400(class='hover:bg-orange-300')
              span Search
          button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
            v-if="title === 'giáo viên'"
            class='hover:bg-green-500 md:mt-0'
            @click="openTeacherDialog('add')"
          )
            span + Thêm {{ title }}
          button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
            v-if="title === 'học sinh'"
            class='hover:bg-green-500 md:mt-0'
            @click="openStudentDialog('add')"
          )
            span + Thêm {{ title }}
          button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
            v-if="title === 'lớp học'"
            class='hover:bg-green-500 md:mt-0'
            @click="openClassroomDialog('add')"
          )
            span + Thêm {{ title }}
        .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
          .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
            table.w-full.whitespace-nowrap.rounded-lg.border
              thead
                tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                  th.px-4.py-3.text-center.border STT
                  th.px-4.py-3.border(v-if="title !== 'lớp học'") Mã gv
                  th.px-4.py-3.border(v-if="title === 'lớp học'") Mã Lớp
                  th.px-4.py-3.border(v-if="title !== 'lớp học'") Họ tên
                  th.px-4.py-3.border(v-if="title === 'lớp học'") Môn
                  th.px-4.py-3.border.text-center(v-if="title !== 'lớp học'") Thông tin
                  th.px-4.py-3.border(v-if="title === 'lớp học'") Gv
                  th.px-4.py-3.border(v-if="title === 'lớp học'") Thông tin
                  th.px-4.py-3.border.text-center Tùy chọn
              tbody.bg-white
                tr.text-gray-700(v-for="(item, index) in data" :key="item.id")
                  td.px-4.py-3.border.text-center {{ index + 1 }}
                  td.px-4.py-3.border.text-center {{ item.id }}
                  td.px-4.py-3.border {{ item.name }}
                  td.px-4.py-3.border(v-if="title === 'lớp học'") {{ item.teacher.name }}
                  td.px-4.py-3.text-sm.border
                    .flex.justify-center
                      button.bg-blue-500.text-white.px-4.py-2.rounded.mt-6(
                        @click="openWatchDialog(item.id)"
                        class='hover:bg-blue-400 md:mt-0'
                      )
                        span Xem
                  td.px-4.py-3.text-sm.border
                    .flex.items-center.justify-center.gap-4
                      button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                        v-if="title === 'giáo viên'"
                        class='hover:bg-green-500 md:mt-0'
                        @click="openTeacherDialog('edit', item)"
                      ) Sửa

                      button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                        v-if="title === 'học sinh'"
                        class='hover:bg-green-500 md:mt-0'
                        @click="openStudentDialog('edit', item)"
                      )
                        span Sửa
                      button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                        v-if="title === 'lớp học'"
                        class='hover:bg-green-500 md:mt-0'
                        @click="openClassroomDialog('edit', item)"
                      )
                        span Sửa
                      button.bg-green-600.text-white.px-4.py-2.rounded.mt-6(
                        v-if="title === 'lớp học'"
                        class='hover:bg-green-500 md:mt-0'
                        @click="openListStudent(item)"
                      )
                        span Thêm học sinh
                      button.bg-red-500.text-white.px-4.py-2.rounded.mt-6(
                        class='hover:bg-red-400 md:mt-0'
                        @click="openDeleteDialog(item)"
                      )
                        span Xóa

    watch-information(
      :value="isOpenWatchDialog"
      :title="'Thông tin chung'"
      :type="title"
      :data="dataWatch"
      @on-close="isOpenWatchDialog = false"
    )

    teacher-dialog(
      :value="isOpenTeacherDialog"
      :title="title"
      :teacher="teacherProp"
      :mode="mode"
      @on-close="isOpenTeacherDialog = false"
      @reload="$emit('reload')"
    )

    student-dialog(
      :value="isOpenStudentDialog"
      :title="title"
      :student="studentProp"
      :mode="mode"
      :classrooms="classrooms"
      @on-close="isOpenStudentDialog = false"
      @reload="$emit('reload')"
    )

    classroom-dialog(
      :value="isOpenClassroomDialog"
      :title="title"
      :classroom="classroomProp"
      :mode="mode"
      @on-close="isOpenClassroomDialog = false"
      @reload="$emit('reload')"
    )

    delete-dialog(
      :value="isOpenDeleteDialog"
      :type="title"
      :data="deleteProp"
      @on-close="isOpenDeleteDialog = false"
      @reload="$emit('reload')"
    )

    choose-property(
      :value="isOpenChooseProperty"
      :title="'Student'"
      :classroom="currentClassroom"
      @on-close="isOpenChooseProperty = false"
      @reload="$emit('reload')"
    )

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import WatchInformation from '@/components/WatchInformation/index.vue'
import TeacherDialog from '@/components/TeacherDialog/index.vue'
import StudentDialog from '@/components/StudentDialog/index.vue'
import ClassroomDialog from '@/components/ClassroomDialog/index.vue'
import DeleteDialog from '@/components/DeleteDialog/index.vue'
import ChooseProperty from '@/components/ChooseProperty/index.vue'

const ManagementComponent = defineComponent({
  props: {
    title: {
      type: String,
      required: true
    },
    data: {
      type: Array,
      required: true
    },
    classrooms: {
      type: Array,
      required: false,
      default: () => []
    }
  },
  components: {
    WatchInformation,
    TeacherDialog,
    StudentDialog,
    ClassroomDialog,
    DeleteDialog,
    ChooseProperty
  },
  setup() {
    const isOpenWatchDialog = ref(false)
    const teacherProp = ref({})
    const studentProp = ref({})
    const classroomProp = ref({})
    const dataWatch = ref(0)
    const isOpenTeacherDialog = ref(false)
    const isOpenStudentDialog = ref(false)
    const isOpenClassroomDialog = ref(false)
    const isOpenDeleteDialog = ref(false)
    const deleteProp = ref<any>({})
    const mode = ref('')
    const isOpenChooseProperty = ref(false)
    const currentClassroom = ref<any>({})

    const openWatchDialog = (data: any) => {
      dataWatch.value = data
      isOpenWatchDialog.value = true
    }

    const openTeacherDialog = (mdo: string, data?: any) => {
      mode.value = mdo
      if (data) {
        teacherProp.value = {
          id: data.id,
          name: data.name,
          gender: data.gender,
          phone: data.account.phone,
          mail: data.account.mail,
          dateOfBirth: data.dateOfBirth
        }
      } else {
        teacherProp.value = {
          id: null,
          name: '',
          gender: '',
          phone: '',
          mail: '',
          dateOfBirth: ''
        }
      }
      isOpenTeacherDialog.value = true
    }

    const openStudentDialog = (mdo: string, data?: any) => {
      mode.value = mdo
      if (data) {
        studentProp.value = {
          id: data.id,
          name: data.name,
          gender: data.gender,
          phone: data.account.phone,
          mail: data.account.mail,
          dateOfBirth: data.dateOfBirth
        }
      } else {
        studentProp.value = {
          id: null,
          name: '',
          gender: '',
          phone: '',
          mail: '',
          dateOfBirth: ''
        }
      }
      isOpenStudentDialog.value = true
    }

    const openClassroomDialog = (mdo: string, data?: any) => {
      mode.value = mdo
      if (data) {
        classroomProp.value = {
          id: data.id,
          name: data.name,
          classTimes: data.classTimes,
          startDate: data.startDate,
          teacher: data.teacher,
          room: data.room,
          students: data.students
        }
      } else {
        classroomProp.value = {
          id: null,
          name: '',
          classTimes: null,
          startDate: null,
          teacher: null,
          room: null,
          students: []
        }
      }
      isOpenClassroomDialog.value = true
    }

    const openDeleteDialog = (data: any) => {
      deleteProp.value = data
      isOpenDeleteDialog.value = true
    }

    const openListStudent = (classroom: any) => {
      currentClassroom.value = classroom
      isOpenChooseProperty.value = true
    }

    return {
      openWatchDialog,
      isOpenWatchDialog,
      teacherProp,
      openTeacherDialog,
      isOpenTeacherDialog,
      mode,
      dataWatch,
      openStudentDialog,
      isOpenStudentDialog,
      studentProp,
      openClassroomDialog,
      classroomProp,
      isOpenClassroomDialog,
      openDeleteDialog,
      isOpenDeleteDialog,
      deleteProp,
      openListStudent,
      isOpenChooseProperty,
      currentClassroom
    }
  }
})

export default ManagementComponent
</script>

<style lang="sass"></style>
