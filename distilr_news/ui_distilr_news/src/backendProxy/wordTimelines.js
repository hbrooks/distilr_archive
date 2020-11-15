const rp = require('request-promise');


const BACKEND_URL = "http://localhost:6001"


const createTimeline = async (naturalLanguageQuery) => {
    const options = {
        uri: `${BACKEND_URL}/timelines`,
        headers: {
            'Content-Type': 'application/json',
        },
        json: {
            q: naturalLanguageQuery
        },
    };
    try {
        const jsonResponse = await rp.post(options);
        return jsonResponse
    } catch (e) {
        console.error(e)
        if (e.statusCode === 406) {
            return e; // TODO: Throw specific error
        }
        throw e;
    }
}


const getTrending = async () => {
    const options = {
        uri: `${BACKEND_URL}/timelines/trending`,
        headers: {
            'Content-Type': 'application/json',
        },
        json: true,
    };
    try {
        const jsonResponse = await rp.get(options);
        return jsonResponse
    } catch (e) {
        console.error(e)
        throw e;
    }
}


export {
    getTrending,
    createTimeline,
}