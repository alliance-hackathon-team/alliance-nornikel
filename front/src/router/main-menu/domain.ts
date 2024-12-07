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
        title: "Search",
        code: "search",
        onClick: () => router.push({name: "search"}),

    },
    {
        title: "Upload",
        code: "upload",
        onClick: () => router.push({name: "upload"}),

    },
    {
        title: "LLM",
        code: "llm",
        onClick: () => router.push({name: "llm"}),
    }
]

export const handleClickOnLogo = () => router.push({name: "search"})
