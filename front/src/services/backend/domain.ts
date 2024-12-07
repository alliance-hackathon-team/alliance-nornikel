import {z} from "zod";

export const TargetFile = z.object({
    title: z.string(),
    content: z.string(),
    extension: z.string(),
    src: z.string(),
}).strict()


export const Source = z.object({
    title: z.string(),
    src: z.string(),
    pages: z.number(),
    quote: z.string().optional().nullable(),
})


export const LLMResponse = z.object({
    content: z.string(),
    sources: Source.array(),
})


export type TargetFile = z.infer<typeof TargetFile>
export type Source = z.infer<typeof Source>
export type LLMResponse = z.infer<typeof LLMResponse>
