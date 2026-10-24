// Injected into the map page inside the Android app.
// WebView cannot save blob:/data: downloads or show the print dialog on its own,
// so file saves (Excel, PDF, Word, JSON) and printing are handed to the app.
(function () {
  if (window.__oporyApp) return;
  window.__oporyApp = true;
  document.documentElement.classList.add('android-app');

  function save(href, name) {
    fetch(href).then(function (r) { return r.blob(); }).then(function (b) {
      var fr = new FileReader();
      fr.onload = function () {
        var s = String(fr.result), i = s.indexOf(',');
        AndroidApp.save(s.slice(i + 1), name || 'file', b.type || 'application/octet-stream');
      };
      fr.readAsDataURL(b);
    }).catch(function (e) { AndroidApp.toast('Не удалось сохранить файл: ' + e); });
  }

  function grab(a) {
    var h = a.href || '';
    if (!(h.indexOf('blob:') === 0 || h.indexOf('data:') === 0)) return false;
    save(h, a.getAttribute('download') || a.download || 'file');
    return true;
  }

  var click = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { if (!grab(this)) click.call(this); };

  var dispatch = EventTarget.prototype.dispatchEvent;
  EventTarget.prototype.dispatchEvent = function (e) {
    if (this instanceof HTMLAnchorElement && e && e.type === 'click' && grab(this)) return true;
    return dispatch.call(this, e);
  };

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[download]');
    if (a && grab(a)) e.preventDefault();
  }, true);

  window.print = function () { AndroidApp.print(); };
})();
