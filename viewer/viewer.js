function draw(){
    var canvas = document.getElementById('tutorial');
    if (!canvas.getContext) {
      console.log('Could not load canvas context');
    } else {
      var ctx = canvas.getContext('2d');

      ctx.fillStyle = "rgb(200,0,0)";
      ctx.fillRect (200, 100, 55, 50);

      ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
      ctx.fillRect (300, 300, 55, 50);

      var img = new Image();
      img.onload = function(){
        ctx.drawImage(img,0,0);
      };
      img.src = 'images/madcat.gif';

      var icon_play = new Image();
      icon_play.onload = function(){
        ctx.drawImage(icon_play, 0, canvas.height - 28);
      };
      icon_play.src = 'images/icon_play.png';

      var icon_pause = new Image();
      icon_pause.onload = function(){
        ctx.drawImage(icon_pause, 28, canvas.height - 28);
      };
      icon_pause.src = 'images/icon_pause.png';

      $.getJSON("http://127.0.0.1:8080/api/v1/games/5066549580791808", function(data) {
        console.log(data);
      });
    }
}
