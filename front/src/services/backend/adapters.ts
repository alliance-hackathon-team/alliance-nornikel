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
}


export function getBackendAdapter(): BackendAdapter {
    return new BackendAdapter()
}