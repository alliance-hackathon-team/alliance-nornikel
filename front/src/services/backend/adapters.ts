import {TargetFile} from "./domain.ts";

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

class BackendAdapter {
    async getTargetFiles(searchString: string): Promise<TargetFile[]> {
        console.log(searchString);
        return fakeData
    }
}


export function getBackendAdapter(): BackendAdapter {
    return new BackendAdapter()
}