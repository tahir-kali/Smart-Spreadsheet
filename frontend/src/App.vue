<template>
  <div id="app">
    <div class="min-h-screen min-w-full flex items-center justify-center bg-gray-100">
      <UploadAndAsk />
      
    </div>
  </div>
</template>

<script>
import UploadAndAsk from './components/UploadAndAsk.vue';

export default {
  name: 'App',
  components: {
    UploadAndAsk
  }
};
</script>

<style>
/* Global styles can be added here */
</style>
