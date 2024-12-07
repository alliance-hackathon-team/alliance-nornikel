export function dropExtraSpacesFromStartAnEnd(s: string): string {
    const searchValue = new Set([
        "\n",
        " ",
    ])


    let start = 0
    for (; start < s.length; start++) {
        if (!searchValue.has(s[start])) break
    }

    let end = s.length - 1
    for (; end >= 0; end--) {
        if (!searchValue.has(s[end])) break
    }
    return s.slice(start, end + 1)
}

export function findUrlsAndConvertIntoHTML(text: string) {
    let urlRegex = new RegExp(/(https?:\/\/[^\s]+)/g)
    return text.replace(urlRegex, function (url) {
        return '<a href="' + url + '">' + url + '</a>'
    })
}

export function findNewStringsAndConvertIntoHTML(text: string) {
    let rexExp = new RegExp('\r?\n', 'g')
    return text.replace(rexExp, '<br />')
}


export interface GetTextWidthOptions {
    font?: string,
    fontSize?: string,
    fontClass?: string,
}

export function getTextWidth(text: string, options: GetTextWidthOptions) {
    if (!options.font) options.font = "Segoe UI"


    const element = document.createElement("span");
    document.body.appendChild(element);

    element.style.font = options.font;
    if (options.fontSize)
        element.style.fontSize = options.fontSize
    if (options.fontClass)
        element.className = options.fontClass

    element.style.height = '0';
    element.style.width = 'auto';
    element.style.position = 'absolute';
    element.style.whiteSpace = 'no-wrap';
    element.innerHTML = text;
    element.style.overflow = "clip"

    const width = Math.ceil(element.clientWidth);
    document.body.removeChild(element);
    return width
}