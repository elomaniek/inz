async function fetchInfo() {
    try {
        const response = await fetch(`http://localhost:8000/api/streams`, {
            method: 'GET',
            credentials: 'same-origin'
        });
        const exam = await response.json();
        return exam;
        } catch (error) {
            console.error(error);
        }
    };
async function renderInfo() {
    const exam = await fetchInfo();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(exam.response, 'text/xml')
    const streams = xmlDoc.querySelectorAll('live');
    streams.forEach(live => {
        const stream = live.querySelector('stream').firstChild.nodeValue;
    console.log(stream);
    });
    //console.log(Object.values(exam)[0])
    console.log(exam);

};

var info = renderInfo();
