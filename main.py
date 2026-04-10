"""
HeartsConnect WebView App
Wraps https://heartsconnect.cc in a native Android WebView.
Built with Python / KivyMD / Buildozer.
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

APP_URL = "https://heartsconnect.cc"


class HeartsConnectApp(App):
    def build(self):
        # Use Android WebView via pyjnius on device,
        # or a WebBrowser fallback on desktop for testing.
        try:
            from android.webview import WebView as AndroidWebView  # noqa: F401
            return _build_android_webview()
        except ImportError:
            # Desktop fallback: open URL in system browser
            import webbrowser
            webbrowser.open(APP_URL)
            return Widget()  # blank canvas (app exits after opening browser)


def _build_android_webview():
    """Create a full-screen Android WebView widget."""
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView         = autoclass("android.webkit.WebView")
    WebViewClient   = autoclass("android.webkit.WebViewClient")
    activity        = autoclass("org.kivy.android.PythonActivity").mActivity
    WebSettings     = autoclass("android.webkit.WebSettings")

    class _Container(Widget):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_once(self._init_webview)

        @run_on_ui_thread
        def _init_webview(self, *args):
            self._wv = WebView(activity)
            settings = self._wv.getSettings()
            # Enable JavaScript (required for the SPA/AJAX parts of the site)
            settings.setJavaScriptEnabled(True)
            # Support localStorage, sessionStorage
            settings.setDomStorageEnabled(True)
            # Allow mixed content (http assets inside https pages) — set to ALWAYS
            settings.setMixedContentMode(0)
            # Zoom controls
            settings.setBuiltInZoomControls(False)
            settings.setSupportZoom(False)
            # User-agent: keep default (WebView UA)
            settings.setUserAgentString(
                "Mozilla/5.0 (Linux; Android 12; Mobile) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Mobile Safari/537.36 HeartsConnectApp/1.0"
            )

            # Override URL loading so every link stays inside the WebView
            wv_client = WebViewClient()
            self._wv.setWebViewClient(wv_client)

            # Load the site
            self._wv.loadUrl(APP_URL)

            # Attach the WebView to the Android layout
            activity.addContentView(
                self._wv,
                autoclass("android.view.ViewGroup$LayoutParams")(
                    -1,  # MATCH_PARENT width
                    -1,  # MATCH_PARENT height
                ),
            )

    return _Container()


if __name__ == "__main__":
    HeartsConnectApp().run()
