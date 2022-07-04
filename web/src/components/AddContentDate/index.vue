<template lang="pug">
  v-dialog(:value="value" max-width="700" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Unit
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close

      .p-4
        v-text-field(
          v-model="slide.title"
          :label="'tiêu đè'"
        )
        v-text-field(
          v-model="slide.url"
          :label="'url'"
        )
        v-text-field(
          v-model="slide.remark"
          :label="'chú thích'"
        )

      v-card-actions
        v-btn.relative-btn(
          :large="!$vuetify.breakpoint.xsOnly"
          block
          @click="onSave()"
        )
          span Lưu

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'
import moment from 'moment'
import { endpoints, toSnakeCase } from 'utils'
import { api } from 'plugins'

const AddContentDate = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    slide: {
      type: Object,
      required: true
    }
  },
  setup(props, { emit, root }) {
    const { $toast } = root
    const modal = ref(false)
    const date = ref(moment(new Date()).format('YYYY-MM-DD'))

    const onSave = async () => {
      try {
        console.log(props.slide)
        await api.post(endpoints.SLIDE, toSnakeCase(props.slide))
        emit('reload')
        emit('on-close')
        $toast.success('Save data successful')
      } catch (e) {
        $toast.error('Save data failed')
      }
    }

    return {
      modal,
      date,
      onSave
    }
  }
})

export default AddContentDate
</script>

<style lang="sass"></style>
