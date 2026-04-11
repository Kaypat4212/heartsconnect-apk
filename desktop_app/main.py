"""
HeartsConnect Desktop App
Loads https://heartsconnect.cc in a native Edge/WebKit window.
Build to .exe:  python build_exe.py
"""
import json
import os

import webview

APP_URL   = "https://heartsconnect.cc"
APP_TITLE = "HeartsConnect"
SETTINGS  = os.path.join(os.path.expanduser("~"), ".heartsconnect_prefs.json")

# ── Branded loading screen shown while the site fetches ─────────────────────
LOADING_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: linear-gradient(145deg, #0f0c29, #302b63, #24243e);
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  height:100vh;
  font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color:#fff;
}
.icon {
  width:90px; height:90px; border-radius:22px;
  background:linear-gradient(135deg, #e91e63 0%, #880e4f 100%);
  display:flex; align-items:center; justify-content:center;
  font-size:46px; margin-bottom:20px;
  box-shadow:0 8px 32px rgba(233,30,99,.4);
  animation:pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { transform:scale(1);    box-shadow:0 8px 32px  rgba(233,30,99,.4); }
  50%     { transform:scale(1.06); box-shadow:0 12px 40px rgba(233,30,99,.6); }
}
h1 { font-size:26px; font-weight:700; letter-spacing:.5px; margin-bottom:6px; }
p  { font-size:13px; color:rgba(255,255,255,.45); margin-bottom:44px; }
.spinner {
  width:34px; height:34px;
  border:3px solid rgba(255,255,255,.08);
  border-top-color:#e91e63; border-radius:50%;
  animation:spin .75s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
</style></head>
<body>
  <div class="icon">&#10084;</div>
  <h1>HeartsConnect</h1>
  <p>Connecting hearts around the world</p>
  <div class="spinner"></div>
</body></html>"""

# ── Keyboard shortcuts injected after each page load ─────────────────────────
KEYBOARD_JS = """
(function(){
  if (window.__hc_kb) return;
  window.__hc_kb = true;
  document.addEventListener('keydown', function(e){
    if (e.key === 'F5')                     { e.preventDefault(); location.reload(); }
    if (e.altKey && e.key === 'ArrowLeft')  { e.preventDefault(); history.back(); }
    if (e.altKey && e.key === 'ArrowRight') { e.preventDefault(); history.forward(); }
  });
})();
"""


class Api:
    """Python <-> JavaScript bridge, accessible as window.pywebview.api"""
    _win = None

    def set_window(self, w):     self._win = w
    def go_back(self):           self._win.evaluate_js("history.back()")
    def go_forward(self):        self._win.evaluate_js("history.forward()")
    def go_home(self):           self._win.load_url(APP_URL)
    def refresh(self):           self._win.evaluate_js("location.reload()")
    def toggle_fullscreen(self): self._win.toggle_fullscreen()


def _load_prefs():
    try:
        with open(SETTINGS) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_prefs(w):
    try:
        with open(SETTINGS, "w") as f:
            json.dump({"width": w.width, "height": w.height}, f)
    except Exception:
        pass


if __name__ == "__main__":
    prefs  = _load_prefs()
    api    = Api()

    window = webview.create_window(
        title=APP_TITLE,
        html=LOADING_HTML,
        js_api=api,
        width=prefs.get("width", 1100),
        height=prefs.get("height", 780),
        min_size=(400, 600),
        resizable=True,
        text_select=True,
    )
    api.set_window(window)

    window.events.loaded += lambda: window.evaluate_js(KEYBOARD_JS)
    window.events.closed += lambda: _save_prefs(window)

    # Load the real site in a background thread once the GUI loop starts
    webview.start(func=lambda w: w.load_url(APP_URL), args=window, debug=False)
