[app]

title = Ocorrencias Policiais
package.name = ocorrencias
package.domain = org.alineamorim

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

# ANDROID CONFIG ESTÁVEL
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True
android.archs = arm64-v8a

log_level = 2

[buildozer]

log_level = 2
warn_on_root = 1
