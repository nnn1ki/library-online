<template>
    <div class="input-group">
      <label :for="name">{{ label }}</label>
      <input
        v-model="value"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :required="required"
        :class="['input', { 'input-error': hasError }]"
        @blur="validate"
      />
      <span v-if="hasError" class="error-text">{{ errorMessage }}</span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InputField',
    props: {
      label: {
        type: String,
        required: true,
      },
      type: {
        type: String,
        default: 'text',
      },
      placeholder: {
        type: String,
        default: '',
      },
      value: {
        type: [String, Number],
        default: '',
      },
      name: {
        type: String,
        required: true,
      },
      required: {
        type: Boolean,
        default: false,
      },
      validateFn: {
        type: Function,
        default: null,
      },
      errorMessage: {
        type: String,
        default: 'This field is required.',
      },
    },
    data() {
      return {
        hasError: false,
      };
    },
    methods: {
      validate() {
        if (this.required && !this.value) {
          this.hasError = true;
        } else if (this.validateFn && !this.validateFn(this.value)) {
          this.hasError = true;
        } else {
          this.hasError = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .input-group {
    margin-bottom: 20px;
  }
  
  .input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .input-error {
    border-color: red;
  }
  
  .error-text {
    color: red;
    font-size: 12px;
  }
  </style>