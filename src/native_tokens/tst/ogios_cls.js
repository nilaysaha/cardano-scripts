const WebSocket = require('ws');
const client = new WebSocket("ws://localhost:1337");

function wsp(methodname, args, mirror) {
    client.send(JSON.stringify({
        type: "jsonwsp/request",
        version: "1.0",
        servicename: "ogmios",
        methodname,
        args,
        mirror
    }));
}

client.once('open', () => {
    const lastByronBlock = {
        slot: 4492799,
        hash: "f8084c61b6a238acec985b59310b6ecec49c0ab8352249afd7268da5cff2a457"
    };
    wsp("FindIntersect", { points: [lastByronBlock] });
});

client.on('message', function(msg) {
    const response = JSON.parse(msg);

    switch (response.methodname) {
    case "FindIntersect":
	if (!response.result.IntersectionFound) { throw "Whoops? First Shelley block disappeared?" }
	for (let i = 14; i > 0; i += 1) {
            wsp("RequestNext", {});
	}
	break;
	
    case "RequestNext":
        if (response.result.RollForward) {
            console.log(response.result);
        }
	
        if (response.reflection.n > 0) {
            wsp("RequestNext", {}, { n: response.reflection.n - 1 });
        } else {
            client.close();
        }
        break;
    }
});
