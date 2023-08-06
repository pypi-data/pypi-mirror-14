/* global console module */
var querystring = require("querystring");

function start(config, base_connection) {
  var fs = require('fs');
  var http = require("http");
  var cookie = require('cookie');
  var app = require('express')();
  var server = require('http').Server(app);
  var io = require('socket.io')(server);
  var sockets = {};

  app.set('trust proxy', true);

  app.get('*', handler);

  if (config.redis) {
      var redis = require('socket.io-redis');
      var adapter = redis(config.redis, config.redisOpts);
      io.adapter(adapter);
  }

  if (config.socket) {
      try {
          fs.unlinkSync(config.socket);
      } catch (ex) {
          // don't care
      }
      server.listen(config.socket);
  } else {
      server.listen(config.port);
  }

  io.on('connection', function (socket) {
    var listen = socket.onevent;
    var socket_id = socket.id;

    try {
      connect(socket, {data: ["connect", {}]});
    } catch(ex) {

    }

    socket.onevent = function (packet) {
      if (packet[0] !== "do") {
        connect(socket, packet);
      }

      // send the packet to the normal socketio stuff
      listen.bind(this)(packet);
    };

    socket.on('do', function(packet) {
      connect(
        socket,
        {data: ["do", packet]},
        null,
        packet.url
      );
    });

    socket.on('disconnect', function (data) {
      // console.log(" < disconnect", socket_id);
      connect(socket, {data: ["disconnect", {}]}, socket_id);
    });
  });

  /** recieve incoming request from the local server */
  function handler(req, res) {
    var event, data;

    console.log(" * got request for", req.url, req.method);

    if (req.method === "GET") {
      event = req.url;
      data = "";

      req.on("data", function(chunk) {
        data += chunk;
      });
      req.on("end", function() {
        try {
          data = JSON.parse(data);
          // console.log(" > task starting:", event, data);

          res.writeHead(200);
          res.end("GOT.");

          connect(
            {id: null, request: req},
            {data: [event, data]},
            null,
            event
          );
        } catch (ex) {
          console.log("");
          console.log("Invalid json:", ex);
          console.log("Data:", data);
          console.log("");
          res.writeHead(500);
          res.end("bad json.");
        }
      });
      req.on("error", function() {
        console.error(" > task failed:", event, data);
        res.writeHead(500);
        res.end("error, sorry.");
      });
    } else if (req.method === "POST") {
      event = req.url.split("/")[1];
      data = "";
      req.on("data", function(chunk) {
        data += chunk;
      });
      req.on("end", function() {
        data = JSON.parse(data);
        if (data.data) {
          data.data.event = event;
        }

        res.writeHead(200);
        res.end("OK.");

        if (data.sockets) {
          data.sockets.forEach(function (id) {
            if (id) {
              try {
                var temp_socket = io.sockets.connected[id];
                if (temp_socket) {
                  // console.log(" > emitting", event, "to", id);//, data.data);
                  temp_socket.emit(event, data.data);
                } else {
                  // console.log(" !", id, "is no longer connected");
                  if (req.headers.cookie) {
                    connect(
                      {id: id, request: req},
                      {data: ["disconnect", {}]}
                    )
                  }
                }
              } catch (ex) {
                console.log("error sending", ex);
              }
            }
          });
        } else if (data.sockets === null) {
          io.sockets.emit(event, data.data);
        }
      });
    } else {
      console.log("confused handler");
      res.writeHead(200);
      res.end("confused.");
    }
  }

  function connect(socket, packet, socket_id, path) {
    var event = packet.data[0];
    var data = packet.data[1] || {};

    // add the socket's id so the backend knows who this is
    if (! socket_id && socket) {
      socket_id = socket.id;
    }

    // update the last connect time
    // might use this in the future to dismiss old clients
    if (socket_id) {
      data.socket = socket_id;
      sockets[socket_id] = new Date().getTime();
    }

    var connection = JSON.parse(base_connection);
    if (! connection.headers) {
      connection.headers = {};
    }

    // pretend to be ajax
    // helps when trying to read errors
    connection.headers['X_REQUESTED_WITH'] = "XMLHttpRequest";

    // identify this server
    connection.headers['X_WEBSOCKET'] = "true";

    // give cookies
    if (socket && socket.request.headers.cookie) {
      connection.headers.Cookie = socket.request.headers.cookie;
    }

    // if cookies is blank it will crashy crashy
    if (! connection.headers.Cookie) {
      delete connection.headers.Cookie;
    }

    if (data.auth_token) {
      connection.headers.Authorization = "Token " + data.auth_token;
      delete data.auth_token;
    }

    if (data.csrftoken) {
      connection.headers["X-CSRFToken"] = data.csrftoken;
      delete data.csrftoken;
    }

    // have to make it a string to send
    data = querystring.stringify(data);

    // content type and length are required or no data will be sent
    connection.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    connection.headers['Content-Length'] = Buffer.byteLength(data);

    if (path) {
      connection.path = path;
    } else {
      connection.path += event;
    }

    // some old configurations might not use this, but it expects this now
    connection.method = "POST";

    // inform the server that we have an event
    var request = http.request(connection, function (response) {
      var resp = "";
      response.on("data", function (chunk) {
        resp += chunk;
      });
      response.on("end", function () {
        if (response.statusCode !== 200) {
          console.log(" ! Badness from", connection.path,
            "returned", response.statusCode, resp.length, ".");
          console.log(resp);
        } else {
          try {
            resp = JSON.parse(resp);
            if (resp.event == "__cmd__") {
              if (resp.join) {
                resp.join.forEach(function(name) {
                  socket.join(name);
                });
              }
              if (resp.leave) {
                resp.leave.forEach(function(name) {
                  socket.leave(name)
                });
              }
            } else {
              if (event !== "disconnect") {
                socket.emit(resp.event || event, resp);
              }
            }
          } catch(e) {
            console.log(" ! response isn't json", resp);
          }
        }
      });
    });

    // write using name value pairs
    request.write(data);

    // if there is an error, inform the client
    request.on("error", function (err) {
      console.log(" ! error sending request", err);
      if (socket_id) {
        socket.emit("error_message", "failed to send event " + err);
      }
    });

    request.end();

    // console.log(" < received:", event, data);
  }
};

module.exports = {
    start: start
};
