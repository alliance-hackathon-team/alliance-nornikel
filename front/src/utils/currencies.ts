interface Currency {
    [index: string]: string,
}

const currency: Currency = {
    "RUB": "₽",
    "USD": "$",
}

export function getCurrencySymbol(code: keyof Currency) {
    return currency[code]
}

export function getAmountString(code: keyof Currency, amount: number): string {
    const symbol = currency[code]
    return amount >= 0 ? `${symbol}${amount}` : `-${symbol}${-amount}`
}