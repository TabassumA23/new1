import App from './App.vue';
import { createApp } from 'vue';
import router from './router/index.ts';
import { createPinia } from 'pinia';
import VueCookies from 'vue3-cookies';


const app = createApp(App);
const pinia = createPinia();


app.use(VueCookies);
app.use(pinia);
app.use(router);
app.mount('#app');
