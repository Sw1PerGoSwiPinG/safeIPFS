import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconVue from '@element-plus/icons-vue'

const app = createApp(App)

app.config.globalProperties.$proxy_server = 'http://10.122.236.111:5000';
app.config.globalProperties.$client_server = 'http://localhost:5000';

for (const [key, component] of Object.entries(ElementPlusIconVue)) {
    app.component(key, component)
}

app.use(store).use(router).use(ElementPlus).mount('#app')
