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
          v-dialog.title-color(
            ref="dialog"
            persistent
            max-width="400"
            :return-value.sync="questionFileProps.date"
            v-model="modal"
          )
            template(v-slot:activator="{ on, attrs }")
              v-text-field.pa-0.pr-1(
                :label="'Bài tập cho ngày'"
                readonly
                hide-details
                append-outer-icon="mdi-calendar"
                v-bind="attrs"
                v-on="on"
                :value="date"
                @click:append-outer="modal = true"
              )
            v-date-picker(full-width scrollable color="rough_black" header-color="rough_black" v-model="date")
              v-spacer
              v-btn(text color="light_red" @click="modal = false")
                span Cancel
              v-btn(text color="rough_black" @click="$refs.dialog.save(date)")
                span Ok
          v-text-field(label="Tiêu đề" v-model="questionFileProps.title" )
          v-row
            v-file-input(
              v-if="!questionFileProps.fileQuestions.id || isEditFile"
              accept="pdf/*, doc/*"
              v-model="file"
            )
          v-row
            v-col
              span.text-click-able(
                v-if="questionFileProps.fileQuestions.id"
                @click="openFile(questionFileProps.fileQuestions.url)"
              ) xem file
            v-col
              v-btn(
                v-if="questionFileProps.fileQuestions.id"
                @click="isEditFile = true"
              ) edit file

        v-card-actions
          v-btn.relative-btn(
            :large="!$vuetify.breakpoint.xsOnly"
            block
            @click="onSave()"
          )
            span Lưu

</template>

<script lang="ts">
import { defineComponent, ref, toRefs, watch } from '@vue/composition-api'
import { endpoints, readFile, toSnakeCase } from 'utils'
import { api } from 'plugins'
import moment from 'moment'

const QuestionFileDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    questionFileProps: {
      type: Object,
      required: true
    },
    classroom: {
      type: Object,
      required: true
    }
  },
  setup(props, { root, emit }) {
    const { $toast } = root
    const file = ref<any>()
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))
    const { questionFileProps } = toRefs(props)
    const modal = ref(false)
    const isEditFile = ref(false)

    const createHomeWorkAPI = async () => {
      isEditFile.value = false
      const body = {
        date: date.value,
        classroom_id: props.classroom.id,
        file_question: questionFileProps.value.fileQuestions.id,
        title: questionFileProps.value.title
      }

      try {
        const { data } = await api.post(`${endpoints.HOME_WORK_FILE}`, body)
        questionFileProps.value.url = data.url
        $toast.success('Save data successful')
        emit('re-load')
        emit('on-close')
      } catch {
        $toast.error('Save data failed')
      }
    }

    const updateHomeWorkAPI = async () => {
      isEditFile.value = false
      const body = {
        date: date.value,
        classroom_id: props.classroom.id,
        file_question: questionFileProps.value.fileQuestions.id,
        title: questionFileProps.value.title
      }
      try {
        const { data } = await api.put(
          `${endpoints.HOME_WORK_FILE}${questionFileProps.value.id}`,
          body
        )
        questionFileProps.value.url = data.url
        $toast.success('Save data successful')
        emit('re-load')
        emit('on-close')
      } catch {
        $toast.error('Save data failed')
      }
    }

    const uploadFile = async () => {
      const payload = await readFile(file.value)
      const body = {
        payload,
        name: file.value.name,
        type: file.value.type,
        size: file.value.size
      }
      try {
        const { data } = await api.post(endpoints.FILE_QUESTION, body)
        questionFileProps.value.fileQuestions = data
      } catch {
        $toast.error('Save data failed')
      }
    }

    const onSave = () => {
      if (questionFileProps.value.id) updateHomeWorkAPI()
      else createHomeWorkAPI()
    }

    const openFile = (url: string) => {
      window.open(url)
    }

    watch(
      () => file.value,
      () => {
        uploadFile()
      }
    )

    return {
      file,
      onSave,
      modal,
      date,
      openFile,
      isEditFile
    }
  }
})

export default QuestionFileDialog
</script>

<style lang="sass">
.text-click-able
  text-decoration: underline
  color: blue
  cursor: pointer
</style>
