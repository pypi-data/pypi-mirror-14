var SwampDragonLive = function (sd, el) {
  var sdc = 'swampdragon-live';
  var sdl = this;
  this.sd = sd;
  this.el = el;
  this.cs = [];
  this.listen = function (el) {
    var nl = el.getElementsByClassName(sdc);
    for (var i = 0; i < nl.length; i++) {
      var n = nl[i];
      for (var j = 0; j < n.classList.length; j++) {
        var c = n.classList[j];
        if (c.lastIndexOf(sdc+'-', 0) === 0) {
          if (sdl.cs.indexOf(c) === -1) {
            sdl.cs.push(c);
            sdl.sd.subscribe(sdc, c, {'key': c}, null, null);
          };
        };
      };
    };
  };
  this.listener = function (channels, message) {
    for (var i = 0; i < channels.length; i++) {
      var c = channels[i];
      var ml = sdl.el.getElementsByClassName(c);
      for (var j = 0; j < ml.length; j++) {
        var m = ml[j];
        m.innerHTML = message.data;
        sdl.listen(m);
      };
    };
  };
  this.sd.onChannelMessage(this.listener);
};
swampdragon.open(function () {
  swampdragon_live = new SwampDragonLive(swampdragon, document);
  swampdragon_live.listen(document);
});
