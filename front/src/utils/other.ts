import {ZodObject, ZodRecord} from "zod";
import {fromError} from "zod-validation-error";

export type UnionType = string | number | boolean | Date | undefined | null

export function getAsNotNullable<T>(item?: T) {
    if (!item) throw Error("UndefinedError")
    return item
}


export function recursive(
    value: object | UnionType,
    keyCallback?: (key: string) => string,
    valueCallback?: (value: UnionType) => any
): object | UnionType {
    if (!keyCallback) keyCallback = (x) => x
    if (!valueCallback) valueCallback = (x) => x

    const result: { [index: string]: any } = {}

    if (
        typeof value === "string" ||
        typeof value === "number" ||
        typeof value === "boolean" ||
        typeof value === "undefined" ||
        value === null
    ) {
        return valueCallback(value as UnionType)
    } else if (Array.isArray(value)) {
        return value.map(x => recursive(x, keyCallback, valueCallback))
    } else if (value instanceof Date) {
        return valueCallback(new Date(value))
    } else if (
        typeof value === "object"
    ) {
        const keys = Object.keys(value as object)
        for (let key of keys) {
            //@ts-ignore
            result[keyCallback(key)] = recursive(value[key], keyCallback, valueCallback)
        }
    } else {
        throw Error(`TypeError: ${typeof value}`)
    }

    return result
}

export function toSnakeCase<T>(obj: object): T {
    const cb = function camelToUnderscore(key: string) {
        const result = key.replace(/([A-Z])/g, " $1");
        return result.split(' ').join('_').toLowerCase();
    }
    return recursive(obj, cb) as T
}

export function toCamelCase<T>(obj: object): T {
    const cb = (str: string) =>
        str.toLowerCase().replace(/([-_][a-z])/g, group =>
            group
                .toUpperCase()
                .replace('-', '')
                .replace('_', '')
        );
    return recursive(obj, cb) as T
}


export function safeParsing<T>(parser: ZodObject<any> | ZodRecord, data: T): T {
    try {
        return parser.parse(data) as T
    } catch (err) {
        const validationError = fromError(err);
        console.error(validationError.toString());
        throw Error("ZodError")
    }
}

export function safeArrayParsing<T>(parser: ZodObject<any>, data: T[]): T[] {
    return data.map(x => safeParsing(parser, x))
}


export function sleep(ms = 0) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


export function useDebounce(callback: (...args: any[]) => void, delay: number) {
    let timer: any = null

    return (...args: any[]) => {
        if (timer) clearTimeout(timer)
        timer = setTimeout(() => {
            callback(...args)
        }, delay)
    }
}

export class Debounce {
    timer: any = null
    delay: number = 0
    callback: (...args: any[]) => Promise<void>

    constructor(callback: (...args: any[]) => Promise<void>, delay: number) {
        this.timer = null
        this.callback = callback
        this.delay = delay
    }

    async execute(...args: any[]) {
        if (this.timer) clearTimeout(this.timer)
        this.timer = setTimeout(async () => {
            await this.callback(...args)
        }, this.delay)
    }

    async executeImmediately(...args: any[]) {
        if (this.timer) {
            clearTimeout(this.timer)
            this.timer = null
            await this.callback(...args)
        }
    }

    stopCurrentExecution() {
        if (this.timer) clearTimeout(this.timer)
    }
}