import {createRouter, createWebHistory} from "vue-router"
import SearchPage from "../views/pages/search-page/search-page.vue";
import UploadPage from "../views/pages/upload-page/upload-page.vue";
import LlmPage from "../views/pages/llm-page/llm-page.vue";


export const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes: [
        {
            path: "",
            component: SearchPage,
            name: "search",
        },
        {
            path: "/upload",
            component: UploadPage,
            name: "upload",
        },
        {
            path: "/llm",
            component: LlmPage,
            name: "llm",
        }
    ],
})


