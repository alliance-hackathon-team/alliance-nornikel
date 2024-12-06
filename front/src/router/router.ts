import {createRouter, createWebHistory} from "vue-router"
import SearchPage from "../views/pages/search-page/search-page.vue";
import UploadPage from "../views/pages/upload-page/upload-page.vue";


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
        }
    ],
})


