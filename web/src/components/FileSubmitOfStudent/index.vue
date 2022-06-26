<template lang="pug">
  div
    v-dialog(:value="value" max-width="500" persistent)
      v-card
        v-card-title.text-h5.title-color.lighten-2
          span Bài Tập
          v-spacer
          v-btn(icon @click="$emit('on-close')")
            v-icon mdi-close
        v-card-text
          div(v-for="student in students")
            v-list-item(@click="openResult(student.url)")
              span {{ student.student.name }}
              v-spacer
              v-icon mdi-chevron-right
            v-divider

</template>

<script lang="ts">
import { defineComponent, ref, watch } from '@vue/composition-api'
import { api } from 'plugins'
import { endpoints, toCamelCase } from 'utils'

const FileSubmitOfStudent = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    questionFileId: {
      type: Number,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const students = ref<any>([])

    const getData = async () => {
      try {
        const { data } = await api.get(
          `${endpoints.FILE_RESULT_STUDENT}?classroom_id=${props.classroom.id}&home_work_file=${props.questionFileId}`
        )
        students.value = toCamelCase(data)
      } catch (e) {
        $toast.error('Get data failed')
      }
    }

    const openResult = (url: string) => {
      window.open(url)
    }

    watch(
      () => props.value,
      async () => {
        await getData()
      }
    )

    return {
      students,
      openResult
    }
  }
})

export default FileSubmitOfStudent
</script>
