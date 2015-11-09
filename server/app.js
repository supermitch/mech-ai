var express = require('express');
var app = express();

app.get('/', function (req, res) {
	res.send('Destroy all humans!');
});

var server = app.listen(3000, function () {
	var port = server.address().port;
	console.log('Fired up at http://localhost:%s, baby', port);
});
