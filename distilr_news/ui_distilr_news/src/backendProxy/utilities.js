
const encodeUrlString = (nativeUrl) => {
    return nativeUrl;
}

const decodeUrlString = (urlString) => {
    return urlString;
}

const parseTimeFromApi = (t) => new Date(t*1000)

export {
    encodeUrlString,
    decodeUrlString,
    parseTimeFromApi
}