var app = require("{{ app }}");

// this node server configuration
var config = {
    //socket: "web.socket",
    port: 8005
};

// where to connect with your django site
var django_connection = JSON.stringify({
    //socketPath: "site.sock",
    host: "localhost",
    port: 8000,
    method: "POST",
    path: "/websockets/" // should be the url you include('websockets.urls')
});


app.start(config, django_connection);
