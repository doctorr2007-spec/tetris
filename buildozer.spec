[app]

title = Tetris
package.name = tetrisgame
package.domain = org.example
version = 1.0.0
description = Classic Tetris Game for Android
author = Your Name
author.email = your.email@example.com

icon.filename = 
presplash.filename = 

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy==2.1.0,cython,android

orientation = portrait
android.permissions = INTERNET

android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30

p4a.branch = develop

android.accept_sdk_license = True
log_level = 2
android.archs = arm64-v8a, armeabi-v7a
fullscreen = 1

android.gradle_dependencies = com.android.support:support-annotations:28.0.0

[buildozer]

log_level = 2
build_dir = .buildozer
bin_dir = ./bin
android.accept_sdk_license = True
