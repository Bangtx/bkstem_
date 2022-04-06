<template lang="pug">
  v-dialog(:value="value" max-width="500" persistent)
    v-card
      v-card-title.text-h5.title-color.lighten-2
        span Privacy Policy
        v-spacer
        v-btn(icon @click="$emit('on-close')")
          v-icon mdi-close
      .p-4(v-if="mode==='see'")
        p Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

      .p-4(v-if="mode==='add'")
        h1 Tran xuan banh
        v-container.padding(fluid)
          v-text-field(
            autocomplete="email"
            label="Email"
            height="100px"
          )

      v-divider
      v-card-actions
        v-spacer
        v-btn.title-color(@click="$emit('on-close')") Gửi

</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'

const NotificationDialog = defineComponent({
  props: {
    value: {
      type: Boolean,
      required: true
    },
    mode: {
      type: String,
      required: false,
      default: 'add'
    }
  },
  setup() {
    return {}
  }
})
export default NotificationDialog
</script>

<style lang="sass">
.title-color
  background-color: beige !important
.padding
  padding: 0 !important
.v-input__slot
  display: block !important
</style>
