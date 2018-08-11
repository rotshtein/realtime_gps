// always return index.html
var http = require('http'),
    fs = require('fs'),
    index = fs.readFileSync(__dirname + '/index.html');
var app = http.createServer(function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(index);
});

// print coordinates on setPosition callback
var socket = require('socket.io').listen(app);
socket.on('connection', function(socket) {
  socket.on('setPosition', function(pos) {
    console.log(pos.lat + "," + pos.lng + ",157.1");
  }); 
});

// wait for new connections
app.listen(4242);
