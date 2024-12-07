import {LLMResponse, TargetFile} from "./domain.ts";
import axios from "axios";
import {convertDocumentToTargetFile, ResponseData, sleep} from "./services.ts";
import {safeParsing} from "../../utils/other.ts";

const fakeData: TargetFile[] = [
    {
        title: "First",
        content: "FirstContent",
        extension: ".png",
        src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcYNTZfm35QdMyQ2jxMD9I_47Ch-f2V-LxeA&s",
    },
    {
        title: "Second",
        content: "SecondContent",
        extension: ".pptx",
        src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcYNTZfm35QdMyQ2jxMD9I_47Ch-f2V-LxeA&s",
    },
    {
        title: "Third",
        content: "ThirdContent",
        extension: ".pdf",
        src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcYNTZfm35QdMyQ2jxMD9I_47Ch-f2V-LxeA&s",
    },
    {
        title: "Four",
        content: "FourthContent",
        extension: ".jpeg",
        src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcYNTZfm35QdMyQ2jxMD9I_47Ch-f2V-LxeA&s",
    },
]
for (let i = 0; i < 100; i++) {
    fakeData.push(
        {
            title: "Title_" + String(i),
            content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has" +
                " been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley" +
                " of type and scrambled it to make a type specimen book. It has survived not only five centuries, but" +
                " also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in " +
                "the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with " +
                "desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            extension: ".jpeg",
            src: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcYNTZfm35QdMyQ2jxMD9I_47Ch-f2V-LxeA&s",
        },
    )
}

class BackendAdapter {
    async getTargetFiles(searchString: string): Promise<TargetFile[]> {
        await sleep(3_000)
        console.log(searchString);
        return fakeData
    }

    async getLLMResponse(searchString: string): Promise<LLMResponse> {
        console.log(searchString)
        await sleep(3_000)
        return {
            content: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " +
                "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an " +
                "unknown printer took a galley of type and scrambled it to make a type specimen book." +
                " It has survived not only five centuries, but also the leap into electronic typesetting, " +
                "remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset" +
                " sheets containing Lorem Ipsum passages, and more recently with desktop publishing software " +
                "like Aldus PageMaker including versions of Lorem Ipsum.\n",
            sources: [
                {title: "Source1", pages: [12, 13], src: "https://google.com"},
                {title: "Source2", pages: [1], src: "https://google.com"},
                {title: "Source3", pages: [2, 3], src: "https://google.com"},
            ],
        }
    }

    async uploadFiles(data: File[]): Promise<void> {
        console.log(data);
    }
}

const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
})


class RealBackendAdapter extends BackendAdapter {

    async getTargetFiles(searchString: string): Promise<TargetFile[]> {
        const data = {text: searchString}
        const url = "/search"
        const response: ResponseData = (await axiosInstance.post(url, data)).data
        const result: TargetFile[] = []
        for (let doc of response.result) {
            if (doc.score >= 10) {
                result.push(
                    convertDocumentToTargetFile(doc)
                )
            }
        }
        return result
    }

    async getLLMResponse(searchString: string): Promise<LLMResponse> {
        const data = {text: searchString}
        const url = "/semanticsearch"
        const response: LLMResponse = (await axiosInstance.post(url, data)).data
        return safeParsing(LLMResponse, response)
    }

    async uploadFiles(files: File[]): Promise<void> {
        const formData = new FormData()
        files.forEach((file) => {
            formData.append("files", file); // Все файлы добавляются с именем "files"
        });
        const headers = {
            "Content-Type": "multipart/form-data",
        }

        try {
            await axiosInstance.post("/upload", formData, {headers})
        } catch (error) {
            console.error(error)
            throw error; // Проброс ошибки для обработки вызывающей стороной
        }
    }
}


export function getBackendAdapter(): BackendAdapter {
    return new RealBackendAdapter()
    // return new BackendAdapter()
}