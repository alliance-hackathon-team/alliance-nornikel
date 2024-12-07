export function assert_eq(actual: any, expected: any) {
    if (actual !== expected) throw Error(`AssertionError: ${actual} !== ${expected}`)
}

export function assert_less(actual: any, expected: any) {
    if (!(actual < expected)) throw Error(`AssertionError: ${actual} >= ${expected}`)
}

export function assert(value:  boolean) {
    if (!value) throw Error(`AssertionError`)
}
