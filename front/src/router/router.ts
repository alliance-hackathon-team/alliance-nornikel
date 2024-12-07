import {createRouter, createWebHistory} from "vue-router"
import UploadPage from "../views/pages/upload-page.vue";
import LlmPage from "../views/pages/llm-page.vue";
import AboutPage from "../views/pages/about-page.vue";


export const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes: [
        {
            path: "/upload",
            component: UploadPage,
            name: "upload",
        },
        {
            path: "/",
            component: LlmPage,
            name: "llm",
        },
        {
            path: "/for-geeks",
            component: AboutPage,
            name: "about",
        },
    ],
})


