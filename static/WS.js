console.log("Awoo");

function lerp(a, b, t) {
    return (1 - t) * a + t * b;
}

function inverseLerp(a, b, v) {
    return (v - a) / (b - a);
}

const clamp = (min, max, num) => Math.min(Math.max(num, min), max);

let url = "ws://" + window.location.host + "/ws";

function startWebsocket() {
    let webSocket = new WebSocket(url);
    webSocket.onmessage = onmessage
    webSocket.onclose = function () {
        // connection closed, discard old websocket and create a new one in 5s
        webSocket = null
        setTimeout(startWebsocket, 5000)
    }
}

startWebsocket();
const eyes = document.getElementsByClassName('eyeTex');

function onmessage(event) {
    let eyeData = JSON.parse(event.data)
    Array.from(eyes).forEach(i => {
        if (Object.hasOwn(eyeData, "eyeX")) {
            i.style.left = clamp(0.5, 99.5, lerp(0.0, 100, inverseLerp(1, 0, eyeData.eyeX))) + '%';
        }
        if (Object.hasOwn(eyeData, "eyeY")) {
            i.style.top = clamp(0.5, 99.5, lerp(0, 100, inverseLerp(1, 0, eyeData.eyeY))) + '%';
        }
    });
}
