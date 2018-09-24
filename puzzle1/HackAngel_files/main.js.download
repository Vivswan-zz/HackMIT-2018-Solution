// Shake.
(function(d){d.fn.shake=function(a){"function"===typeof a&&(a={callback:a});a=d.extend({direction:"left",distance:20,times:3,speed:140,easing:"swing"},a);return this.each(function(){var b=d(this),k={position:b.css("position"),top:b.css("top"),bottom:b.css("bottom"),left:b.css("left"),right:b.css("right")};b.css("position","relative");var c="up"==a.direction||"down"==a.direction?"top":"left",e="up"==a.direction||"left"==a.direction?"pos":"neg",f={},g={},h={};f[c]=("pos"==e?"-=":"+=")+a.distance;g[c]=
("pos"==e?"+=":"-=")+2*a.distance;h[c]=("pos"==e?"-=":"+=")+2*a.distance;b.animate(f,a.speed,a.easing);for(c=1;c<a.times;c++)b.animate(g,a.speed,a.easing).animate(h,a.speed,a.easing);b.animate(g,a.speed,a.easing).animate(f,a.speed/2,a.easing,function(){b.css(k);a.callback&&a.callback.apply(this,arguments)})})}})(jQuery);

// Sync.
var videos = {
    a: Popcorn("#b"),
    b: Popcorn("#a"),
  },
  loadCount = 0,
  events = "play pause timeupdate seeking".split(/\s+/g);

// iterate both media sources
Popcorn.forEach(videos, function(media, type) {

  // when each is ready... 
  media.on("canplayall", function() {
    // trigger a custom "sync" event
    this.emit("sync");

    // Listen for the custom sync event...    
  }).on("sync", function() {

    // Once both items are loaded, sync events
    if (++loadCount == 2) {

      // Iterate all events and trigger them on the video B
      // whenever they occur on the video A
      events.forEach(function(event) {

        videos.a.on(event, function() {
            if ($("#b").length == 0) return;
        

          // Avoid overkill events, trigger timeupdate manually
          if (event === "timeupdate") {

            if (!this.media.paused) {
              return;
            }
            videos.b.emit("timeupdate");

            return;
          }

          if (event === "seeking") {
            videos.b.currentTime(this.currentTime());
          }

          if (event === "play" || event === "pause") {
            videos.b[event]();
          }
        });
      });
    }
  });
});

function sync() {
  if ($("#b").length == 0) return;
  if (videos.b.media.readyState === 4) {
    videos.b.currentTime(
      videos.a.currentTime()
    );
  }
  requestAnimationFrame(sync);
}

sync();

// Actual stuff.
$(".angel-button-i").click(() => {
    $(".entry2").fadeOut();
    $("#b").get(0).play();
});

$(".filter").click(() => {
    $(".filter").shake();
    console.log("Couldn't disable filter :(");
});