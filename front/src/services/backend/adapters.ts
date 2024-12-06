import {TargetFile} from "./domain.ts";
import axios from "axios";
import {convertDocumentToTargetFile, ResponseData} from "./services.ts";

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
        console.log(searchString);
        return fakeData
    }

    async uploadFiles(data: File[]): Promise<void> {
        console.log(data);
    }
}

const axiosInstance = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Accept": "application/json",
    },
})


class RealBackendAdapter extends BackendAdapter {

    async getTargetFiles(searchString: string): Promise<TargetFile[]> {
        const data = {text: searchString}
        const url = "/search"
        const response: ResponseData = (await axiosInstance.post(url, data)).data
        const result: TargetFile[] = []
        for (let doc of response.result) {
            if (doc.score >= 10){
                result.push(
                    convertDocumentToTargetFile(doc)
                )
            }
        }
        return result
    }

    async uploadFiles(files: File[]): Promise<void> {
        const formData = new FormData()
        files.forEach((file, index) => {
            formData.append(`files[${index}]`, file); // Вложение файла с индексированием
        })
        const headers = {
            "Content-Type": "multipart/form-data",
        }

        try {
            await axiosInstance.post(
                "/upload",
                formData,
                {headers: headers,},
                )

        } catch (error) {
            console.error(error)
            throw error; // Проброс ошибки для обработки вызывающей стороной
        }
    }
}


export function getBackendAdapter(): BackendAdapter {
    return new RealBackendAdapter()
}