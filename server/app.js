var express = require('express');
var app = express();

app.get('/', function (req, res) {
	res.send('Destroy all humans!');
});

app.get('/game', function (req, res) {
	var game = {
		game: 'Destroy all humans!'
	};
	res.send(game);
});

var server = app.listen(3000, function () {
	var port = server.address().port;
	console.log('Fired up at http://localhost:%s, baby', port);
	console.log('Try http://localhost:%s/', port);
	console.log('Try http://localhost:%s/game', port);
});
