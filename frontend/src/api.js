// functions for calling the python API

// I ran into problems designing this, I was expecting there to be
// a simple way to let the server know that repeated requests
// were coming from the same source
// I researched a fair bit but couldn't find a solution,
// so instead I send a custom session ID
// this is a poor solution as it's not secure at all


export function postPlay(sessionID, sessionCredit) {
    return fetch(
        'http://127.0.0.1:8000/play/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-session-id': sessionID
            },
            body: JSON.stringify({
                account_credit: sessionCredit,
            }),
            // I thought setting this credentials option
            // would avoid the need to send a custom header
            // with the session ID, but I couldn't get it to work
            // https://developer.mozilla.org/en-US/docs/Web/API/fetch#credentials
            credentials: 'include'
        }
    ).then(response => response.json())
}

export function getCashOut(sessionID) {
    return fetch(
        'http://127.0.0.1:8000/cash_out/',
        {
            method: 'GET',
            headers: {
                'x-session-id': sessionID,
            },
        }
    ).then(response => response.json())
}
