import {TargetFile} from "./domain.ts";
import {safeParsing} from "../../utils/other.ts";

interface Metadata {
    "file_path": string,
    "title": string,
    "extension": string,
    "size": number,
    "last_modified": string,
    "last_accessed": string,
    "creation_time": string,
    "mode": number,
    "inode": number,
    "device": number,
    "links": number,
    "uid": number,
    "gid": number
}

interface Document {
    "doc_id": 1,
    "page_num": 1,
    "score": 10.1875,
    "metadata": Metadata[],
    "base64": any,
}

export interface ResponseData {
    "result": Document[],
}


export function convertDocumentToTargetFile(data: Document): TargetFile {
    return safeParsing(TargetFile, {
        src: data.metadata[0].file_path,
        title: data.metadata[0].title,
        extension: data.metadata[0].extension,
        content: String(data.page_num),
    })
}


export function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}