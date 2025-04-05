/* 
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia, Pinia } from 'pinia';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App)
const pinia: Pinia = createPinia()

app.use(router)
app.use(pinia)

app.mount('#app')
*/
import App from './App.vue';
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import router from './router/index.ts';
import { createPinia } from 'pinia';

import routes from './router/index.ts'; // Ensure the correct path to the routes file

const app = createApp(App);
const pinia = createPinia();



app.use(pinia);
app.use(router);
app.mount('#app');
