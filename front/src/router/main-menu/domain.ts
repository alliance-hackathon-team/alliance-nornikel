import {router} from "../router.ts";


interface MenuItem {
    title: string,
    code: string,
    onClick: () => void,
    iconCode?: string,
    inMobile?: boolean,
}


export const unauthMenuItems: MenuItem[] = [
    {
        title: "Чат",
        code: "llm",
        onClick: () => router.push({name: "llm"}),
    },
    {
        title: "Файлы",
        code: "upload",
        onClick: () => router.push({name: "upload"}),
    },
    {
        title: "Технарям",
        code: "about",
        onClick: () => router.push({name: "about"}),
    }
]

export const handleClickOnLogo = () => router.push({name: "llm"})
