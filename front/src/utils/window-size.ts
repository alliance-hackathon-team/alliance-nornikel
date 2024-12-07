import {ref} from "vue";

export const windowWidth = ref(screen.width)
window.addEventListener("resize", () => windowWidth.value = screen.width)

export function isMobile() {
    return windowWidth.value < 600
}