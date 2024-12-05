import {z} from "zod";

export const TargetFile = z.object({
    title: z.string(),
    content: z.string(),
    extension: z.string(),
    src: z.string(),
}).strict()

export type TargetFile = z.infer<typeof TargetFile>

