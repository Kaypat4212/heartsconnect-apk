[app]

# ── App identity ────────────────────────────────────────────────────────────
title           = HeartsConnect
package.name    = heartsconnect
package.domain  = cc.heartsconnect

# Source directory (relative to this spec file)
source.dir      = .
source.include_exts = py,png,jpg,kv,atlas

version         = 1.0.0

# ── Requirements ────────────────────────────────────────────────────────────
# pyjnius is needed to call Android WebView APIs via JNI
requirements = python3,kivy,pyjnius

# ── Orientation & window ────────────────────────────────────────────────────
orientation     = portrait
fullscreen      = 0

# ── Android permissions ─────────────────────────────────────────────────────
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Target / minimum SDK
android.api         = 33
android.minapi      = 21
android.ndk         = 25b
android.sdk         = 33

# ── Icons & splash ──────────────────────────────────────────────────────────
# Place your 512×512 icon as apk/icon.png to override the default
# icon.filename     = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png
# presplash.color = #e91e63

# ── Build settings ──────────────────────────────────────────────────────────
android.release_artifact = apk
android.debug_artifact   = apk

# Enable AndroidX
android.enable_androidx  = True

# Accept Android SDK licenses automatically during build
android.accept_sdk_license = True

# ── Buildozer internal ──────────────────────────────────────────────────────
[buildozer]
log_level = 2
warn_on_root = 1
