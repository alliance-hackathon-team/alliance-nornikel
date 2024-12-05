import {createApp} from 'vue'
import {router} from "./router/router"
import App from './App.vue'
import {createPinia} from 'pinia'
import VueClickAway from "vue3-click-away"

import "./views/assets/css/colors.css"
import "./views/assets/css/fonts.css"
import "./views/assets/css/buttons.css"
import "./views/assets/css/inputs.css"
import "./views/assets/css/margins.css"
import "./views/assets/css/checkboxes.css"
import "./views/assets/css/cards.css"
import "./views/assets/css/layout.css"
import "./views/assets/css/cursors.css"
import "./views/assets/css/page-layout.css"
import "./views/assets/css/borders.css"
import "./views/assets/css/other.css"


const app = createApp(App)
const pinia = createPinia()

app
    .use(router)
    .use(pinia)
    .use(VueClickAway)
    .mount('#app')
