[app]

title = Ocorrencias Policiais
package.name = ocorrencias
package.domain = org.alineamorim

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# --- Android config estável ---
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True

# Evita build-tools 37
android.gradle_dependencies =

# Arquiteturas
android.archs = arm64-v8a, armeabi-v7a

# Log level
log_level = 2

# Build mode
android.release_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
