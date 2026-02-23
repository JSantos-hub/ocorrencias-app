[app]

title = SistemaOcorrencias
package.name = sistemaocorrencias
package.domain = org.institucional

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,kivymd,plyer,reportlab,bcrypt,requests

orientation = portrait

fullscreen = 0

android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION

android.api = 33
android.minapi = 21

android.arch = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.logcat_filters = *:S python:D

[buildozer]

log_level = 2
warn_on_root = 1
