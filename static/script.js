const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = function (event) {
  console.log(event.data);
}

ws.onmessage = function (event) {
  console.log(event.data);
}