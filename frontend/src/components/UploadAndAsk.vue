<template>
  <div class="w-full border mx-auto p-4 absolute top-0">
    
    <h1 class="text-2xl font-bold mb-4">Smart Spreadsheet</h1>
    
    <div class="h-[calc(100vh_-_300px)] overflow-y-auto">
      
      <div v-for="(conversation,key) in conversations" :key="key" class="my-2 w-full">
        <div :class="['flex',{'justify-end':conversation.sender=='you','justify-start':conversation.sender=='system'},'w-full']">
          <div :class="[{'bg-blue-500 text-white':conversation.sender =='system','bg-slate-200':conversation.sender=='you'},'rounded-lg p-4 max-w-xs mb-4 w-auto']">
            <p class="text-sm" v-html="conversation.message"></p>
          </div>
        </div>
      </div>
      
    </div>
    
    <!-- <textarea v-model="question" placeholder="Ask a question about the spreadsheet..." class="w-full mb-4 p-2 border rounded"></textarea> -->
    <!-- <button :disabled="!uploaded_paths.length" @click="askQuestion" class="px-4 py-2 bg-blue-500 text-white rounded">Ask</button> -->
    <div class="w-full flex border rounded-full shadow-sm p-2 bg-white">
      <input type="text" v-model="question" placeholder="Ask a question about the spreadsheet..." class="w-full py-2 pl-4 pr-10  focus:outline-none focus:none focus:none focus:border-transparent">
      <button @click="askQuestion" class="transform -translate-y-1/14 bg-blue-500 hover:bg-blue-700 text-white font-bold p-2 rounded-full shadow-lg transition-transform duration-200 ease-in-out hover:scale-105 focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
        </svg>
      </button>
    </div>
    <div>
      <div class="flex justify-end overflow-x-auto h-[60px] my-2">
        <div class="flex justify-start w-full">
          <div v-for="(path,key) in uploaded_paths" :key="key" class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
          <span class="font-medium">+</span> {{path}}
        </div>
        </div>
        <div class="text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400 w-[200px] border absolute mt-2">
          <label class="w-full cursor-pointer bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700">
            <input type="file" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" @change="handleFileUpload">
            + Upload Spreadsheets
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref,reactive } from 'vue';
const instructions = [
{
  "sender": "system",
  "message": "👋 Welcome to Smart Spreadsheet AI Onboarding! Here's a quick guide to get started: 1. Log in with your credentials. 2. Upload Excel files. Our AI will analyze them. 3. Ask questions about your data. 4. Get accurate, timely answers.",
  "timestamp": "2024-06-10T09:00:00"
},
{
  "sender": "system",
  "message": "5. Explore additional features. 6. Provide feedback. 7. Enjoy the benefits of Smart Spreadsheet AI. If you need help, contact us. Welcome aboard!",
  "timestamp": "2024-06-10T09:01:00"
}
]

const conversations = reactive([...instructions])
const question = ref('');
const uploaded_paths = reactive([]);
const handleFileUpload = async (event) => {
  try {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    if(data.path){
      uploaded_paths.push(data.path)
      conversations.push({
        sender: "you",
        message: "File uploaded successfully!"
      })
    }
    console.log('File uploaded successfully');
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};

const askQuestion = async () => {
  try {
    conversations.push({
      sender: "you",
      message: question.value
    })
    console.log(`Some data here ${JSON.stringify(uploaded_paths)}`)
    const response = await fetch('/api/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question: `${question.value}. Only respond with html code and nothing else if you're asked for html code in previous sentence.`,files: uploaded_paths })
    });
    
    const data = await response.json();
    
    conversations.push({
      sender: "system",
      message: data.answer,
      data: data.data
    })
  } catch (error) {
    console.error('Error:', error);
  }
};
</script>

<style scoped>
/* Additional styles can be added here */
</style>
