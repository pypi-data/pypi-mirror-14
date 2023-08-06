var explodesize = 128;

$(document).ready(function() {
    $(document.body).append('<img width="'+explodesize+'px" height="'+explodesize+'px" id="asplosion" src="http://pappy/static/explosion.gif" style="position:absolute" />');
    $("#asplosion").hide()
});

function explode(x, y) {
    console.log("exploding");
    $("#asplosion").show()
    $("#asplosion").css({"left" : x-explodesize/2, "top" : y-explodesize/2});
    setTimeout(function() { $("#asplosion").hide() }, 1300);
}

$(document).click(function (e) {
    if (e.button == 0) {
        explode(e.pageX, e.pageY);
    }
});
