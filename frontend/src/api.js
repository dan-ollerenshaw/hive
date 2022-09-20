// functions for calling the python API

export function getDummy() {
    console.log("getting dummy endpoint")
    return fetch(
        'http://127.0.0.1:8000/dummy/',
        {
            method: 'GET',
        }
    ).then(response => response.json())
}
