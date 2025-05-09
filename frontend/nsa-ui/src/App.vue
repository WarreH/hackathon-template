<script setup lang="ts">
import { Button } from "@/components/ui/button"
import {ref} from "vue";
import {callApi} from "@/lib/api.ts";
import { Input } from '@/components/ui/input'


const promptAnswer = ref<string | null>(null);
    const userInput = ref('Generate a raw <svg> element (no escaping, no XML declaration) containing a visually interesting abstract shape using basic elements like <circle>, <rect>, <polygon>, or <path>. It should be colorful, compact, and ready to paste directly into an HTML page. Do not include explanations or extra text. Don\'t wrap it in triple backticks or specify a language. Just return the raw <svg> block with no Markdown formatting.');

    const getPrediction = async () => {
      try {
        const response = await callApi<{ result: any }>('http://127.0.0.1:8080/'+userInput.value.toString(), 'GET');
        promptAnswer.value = response.response;
      } catch (error) {
        console.error('API error:', error);
        promptAnswer.value = 'Error fetching result';
      }
    };

</script>

<template>
  <div>
    <div>
    <Button @click="getPrediction">Get result prompt</Button>
    <div v-if="promptAnswer" v-html="promptAnswer"></div>
      <Input
      v-model="userInput"
      type="text"
      placeholder="Enter prompt"
    />
  </div>

  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
