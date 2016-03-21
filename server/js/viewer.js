function draw() {
    var canvas = document.getElementById('tutorial');

    var transactions;

    if (!canvas.getContext) {
        console.log('Could not load canvas context');
    } else {
        draw_ui(canvas);
        var hit_regions = draw_controls(canvas);

        $.when($.getJSON('http://127.0.0.1:8080/api/v1/games/5066549580791808', function() {
            console.log('Initiated');
        }, function() {
            console.log('Error loading game JSON data');
        })).then(function(data) {
            console.log('Get JSON ready!');
            console.log('Data:', data);
            transactions = extract_transactions(data);  // Global?
            console.log('Transactions:', transactions);
            render_map(canvas, transactions[0].state.map);
            var current_frame = 0;
        });
    }

    canvas.addEventListener('click', function(e){
        if (point_collision(e, hit_regions)) {
            alert('Hit a button');
        }
        current_frame = 0;
        render_players(transactions[current_frame].state.players);
    });
}

function draw_ui(canvas) {
    // stuff
}

function draw_controls(canvas) {
    // Render play control images.
    var ctx = canvas.getContext('2d');

    var icon_play = new Image();
    icon_play.onload = function(){ ctx.drawImage(icon_play, 0, canvas.height - 28); };
    icon_play.src = '/images/icon_play.png';

    var icon_pause = new Image();
    icon_pause.onload = function(){ ctx.drawImage(icon_pause, 28, canvas.height - 28); };
    icon_pause.src = '/images/icon_pause.png';

    var hit_regions = {
        'play': {'x': 0, 'y': canvas.height - 28, 'w': icon_play.width, 'h': icon_play.height},
        'pause': {'x': 28, 'y': canvas.height - 28, 'w': icon_play.width, 'h': icon_play.height}
    };
    return hit_regions
}

function render_map(canvas, map) {
    /// Render the map tiles
    var ctx = canvas.getContext('2d');
    var w = 10, h = 10;  // tile width and height
    var x = 0, y = 0;  // tile position

    var red = 'rgb(200, 0, 0)';
    var green = 'rgb(0, 200, 0)';
    var blue = 'rgb(0, 0, 200)';
    var light = 'rgb(200, 200, 200)';

    console.log('Map:', JSON.stringify(map));
    var rows = map.split('\n');
    console.log('Rows:', rows);

    var col = 0;
    rows.forEach(function(row) {
        col++;
        for (var i = 0; i < row.length; i++) {
            var c = row.charAt(i);
            switch (c) {
                case '.': colour = light; break;
                case '*': colour = blue;  break;
                case '@': colour = green; break;
                default:  colour = red;
            }
            ctx.fillStyle = colour;
            x = i * w;
            y = col * h;
            ctx.fillRect(x, y, w, h);

            ctx.lineWidth = 0.2;
            ctx.strokeRect(x, y, w, h);
        }
    });


    ctx.fillStyle = blue;
    x = 100; y = 50;
    ctx.fillRect (x, y, w, h);
}


function render_players(players) {
    for (var name in players) {
        var player = players[name];
        console.log('Player:', player);
    };
}

function extract_transactions(data) {
    // Only return the transactions we need.
    return data.results[0].transactions;
}

function point_collision(e, hit_regions) {
    console.log(e);
    for (var key in hit_regions) {
        if (hit_regions.hasOwnProperty(key)) {
            region = hit_regions[key];
            if (region.y - region.width < e.clientX && region.x + region.width > e.clientX &&
                region.y - region.height < e.clientY && region.y + region.height > e.clientY) {
                return true;
            }
        }
    }
    return false;  // No region was under mouse click
}
