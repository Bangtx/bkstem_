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
      v-list-item(v-for="(unit, index) in units" :key="index")
        span {{ index + 1 }}: {{ unit.title }}
        v-spacer
        v-icon(v-if="member.typeMember === 'teacher'" @click="openBottomSheet(unit)") mdi-dots-vertical
      button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
        v-if="member.typeMember === 'teacher'"
        class='hover:bg-orange-300 focus:outline-none'
        @click="openUnitDialog('add')"
      )
        span.text-base Thêm Unit
      h1.py-2.flex.gap-2.items-center
        div Danh sách sinh viên
      // Danh sách sinh viên
      .w-full.overflow-hidden.rounded-lg.shadow-xs.mt-4(class='lg:px-10')
        .w-full.overflow-auto.rounded-lg(style='max-height: 600px;')
          table.w-full.whitespace-nowrap.rounded-lg.border
            thead
              tr.text-md.font-semibold.text-left.text-gray-900.bg-gray-100.uppercase.border-b.border-gray-600.rounded-t-lg
                th.px-4.py-3.text-center.border STT
                th.px-4.py-3.border Tiêu đề
                th.px-4.py-3.border File
                th.px-4.py-3.border Ghi chú
            tbody.bg-white(v-for="(slide, index) in slides" :key="slide.id")
              tr.text-gray-700
                td.px-4.py-3.border.text-center {{ index }}
                td.px-4.py-3.border {{ slide.title }}
                td.px-4.py-3.text-sm.border(@click="openFile(slide.url)") xem
                td.px-4.py-3.text-sm.border {{ slide.remark }}

      button.mt-4.flex.items-center.justify-between.px-4.py-2.font-medium.leading-5.text-white.transition-colors.duration-150.bg-orange-400.border.border-transparent.rounded-lg(
        v-if="member.typeMember === 'teacher'"
        class='hover:bg-orange-300 focus:outline-none'
        @click="openSlideDialog()"
      )
        span.text-base Thêm Bài giảng

    v-bottom-sheet(
        v-model="showBottomSheet"
        persistent
      )
        div.ma-0.pa-0
          v-row.ma-0.py-0.px-1(align='center' justify='center')
            v-btn.mb-1.rounded-lg(
              block
              height="50"
              elevation="0"
              color="white"
              @click="openUnitDialog('edit')"
            )
              span Sửa
          v-row.ma-0.py-0.px-1(align='center' justify='center')
            v-btn.mb-1.rounded-lg(
              block
              height="50"
              elevation="0"
              color="white"
              @click="showBottomSheet = false"
            )
              span Thoát

    unit-dialog(
      :value="isOpenUnitDialog"
      :classroom="classroom"
      :unit-props="unitProps"
      @re-load="reload()"
      @on-close="isOpenUnitDialog = false"
    )

    add-content-date(
      :value="isOpenSlideDialog"
      :slide="slideProps"
      @on-close="isOpenSlideDialog = false"
      @reload="reload"
    )
</template>

<script lang="ts">
import { defineComponent, ref, watch } from '@vue/composition-api'
import { UnitDialog, AddContentDate } from 'components'
import jwtDecode from 'jwt-decode'
import { toCamelCase } from 'utils'

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
    },
    units: {
      type: Array,
      required: true
    },
    slides: {
      type: Array,
      required: true
    }
  },
  components: {
    UnitDialog,
    AddContentDate
  },
  setup(props, { emit, root }) {
    const { $toast } = root
    const isOpenUnitDialog = ref(false)
    const currentUnit = ref<any>({})
    const showBottomSheet = ref(false)
    const unitProps = ref<any>({})
    const member: any = toCamelCase(jwtDecode(String(localStorage.getItem('token'))))
    const isOpenSlideDialog = ref(false)

    const slideProps = ref({
      title: null,
      classroom: null,
      url: null,
      remark: null
    })

    const openUnitDialog = (mode: string) => {
      if (mode === 'add') unitProps.value = { id: null, name: null }
      else unitProps.value = currentUnit.value
      isOpenUnitDialog.value = true
    }

    const openSlideDialog = () => {
      isOpenSlideDialog.value = true
    }

    const reload = () => {
      emit('re-load')
    }

    const openBottomSheet = (unit: any) => {
      currentUnit.value = unit
      showBottomSheet.value = true
    }

    const openFile = (url: string) => {
      window.open(url)
    }

    watch(
      () => props.classroom,
      () => {
        slideProps.value.classroom = props.classroom.id
      }
    )

    return {
      openUnitDialog,
      isOpenUnitDialog,
      reload,
      openBottomSheet,
      showBottomSheet,
      unitProps,
      member,
      openSlideDialog,
      isOpenSlideDialog,
      slideProps,
      openFile
    }
  }
})

export default ClassHome
</script>
