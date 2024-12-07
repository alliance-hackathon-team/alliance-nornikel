export function toInputDatetimeString(date: Date, format?: string): string {
    const getValue = (n: number, count: number) => {
        let s = String(n)
        if (s.length < count) s = Array(count - s.length).fill(0).join("") + s
        return s
    }
    const year = getValue(date.getFullYear(), 4)
    const month = getValue(date.getMonth() + 1, 2)
    const day = getValue(date.getDate(), 2)
    const hours = getValue(date.getHours(), 2)
    const minutes = getValue(date.getMinutes(), 2)

    let result = ""
    switch (format) {
        case "datetime":
            result = `${year}-${month}-${day}T${hours}:${minutes}`
            break
        case "date":
            result = `${year}-${month}-${day}`
            break
        default:
            result = `${year}-${month}-${day}`
    }
    return result
}

export function fromInputString(s: string): Date {
    const date = s.split("T")[0]
    const time = s.split("T")[1]

    const splitDate = date.split("-")
    const result = new Date(
        Number(splitDate[0]),
        Number(splitDate[1]),
        Number(splitDate[2]),
    )
    if (time) {
        const splitTime = time.split(":")
        result.setHours(Number(splitTime[0]))
        result.setMinutes(Number(splitTime[1]))
    }
    return result
}

export type DatePeriod = (
    "last_day"
    | "last_week"
    | "last_month"
    | "last_year"
    | "next_day"
    | "next_week"
    | "next_month"
    | "next_year"
    )

export function getDatePeriods(code: DatePeriod): [Date, Date] {
    let end = new Date()
    let start = new Date()

    switch (code) {
        case "last_day":
            start.setDate(start.getDate() - 1)
            break
        case "last_week":
            start.setDate(start.getDate() - 7)
            break
        case "last_month":
            start.setMonth(start.getMonth() - 1)
            break
        case "last_year":
            start.setFullYear(start.getFullYear() - 1)
            break
        case "next_day":
            start.setDate(start.getDate() + 1)
            break
        case "next_week":
            end.setDate(end.getDate() + 7)
            break
        case "next_month":
            end.setMonth(end.getMonth() + 1)
            break
        case "next_year":
            end.setFullYear(end.getFullYear() + 1)
            break
        default:
            throw Error(`${code}`)
    }

    return [start, end]

}