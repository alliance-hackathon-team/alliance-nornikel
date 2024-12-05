import {createRouter, createWebHistory} from "vue-router"
import SearchPage from "../views/pages/search-page.vue";


export const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: 'active',
    routes: [
        {
            path: "",
            component: SearchPage,
            name: "search",
        },
    ],
})


