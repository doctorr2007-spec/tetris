[app]

title = Tetris
package.name = tetrisgame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.0.0,android
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.0.0
fullscreen = 1

# Ключевые изменения для обхода ошибки
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

log_level = 2

[buildozer]
log_level = 2
