[app]

# (str) Title of your application
title = Tetris Game

# (str) Package name
package.name = tetrisgame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.tetrisgame

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,glsl

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*, images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv, .git, .buildozer

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license, images/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# !!! ЭТО САМАЯ ВАЖНАЯ ЧАСТЬ - ИСПРАВЛЕННЫЕ ВЕРСИИ !!!
requirements = python3==3.11.9,kivy==2.1.0,cython==0.29.36,android

# (str) Custom source folders for requirements
# requirements.source.kivy = kivy

# (str) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (bool) Indicate if the application should be resizable or not
resizable = 0

#
# Android specific
#

# (bool) Indicate if the application should be a service (background) or not
android.service = False

# (list) Permissions
# android.permissions = INTERNET

# (list) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (int) Android API to use (30 - Android 11, 31 - Android 12, 33 - Android 13)
# !!! ОСТАВЛЯЕМ 30 (СТАБИЛЬНО) !!!
android.api = 30

# (int) Minimum API required (21 = Android 5.0, достаточно для большинства устройств)
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
# !!! ОБЯЗАТЕЛЬНО 25b (НЕ 28c) !!!
android.ndk = 25b

# (str) Android NDK directory (if empty, it will be downloaded)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be downloaded)
# android.sdk_path =

# (str) Ant directory (if empty, it will be downloaded)
# android.ant_path =

# (str) Android entry point (don't change)
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name of the Java class that will act as the entry point for the app
# android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the app
# android.add_src =

# (list) List of Java files to add to the app
# android.add_java =

# (list) List of Java .aar files to add to the app
# android.add_aars =

# (list) List of directories to add to the Java classpath
# android.add_jars =

# (list) List of additional Java directories to add to the classpath
# android.add_src =

# (list) List of Gradle dependencies to add to the build
# android.gradle_dependencies =

# (list) List of additional Java packages to add to the app
# android.add_packages =

# (list) List of Gradle repositories to add to the build
# android.add_repositories =

# (str) Android NDK API to use (the minimum Android version your app will support)
# !!! ОСТАВЛЯЕМ 21 (МИНИМАЛЬНАЯ) !!!
android.ndk_api = 21

# (bool) Use AndroidX instead of Android Support Library
android.use_androidx = true

# (bool) Enable AndroidX auto import feature
# android.enable_androidx_auto_import = false

# (str) Android TV category (leave empty for non-TV)
# android.tv_category = android.intent.category.LEANBACK_LAUNCHER

# (str) Android app theme
# # Available themes: Theme.NoTitleBar, Theme.NoTitleBar.Fullscreen, Theme.Black, Theme.Black.NoTitleBar, Theme.Black.NoTitleBar.Fullscreen
# android.theme = android:style/Theme.NoTitleBar

# (str) Android app widget provider (don't change if you don't know)
# android.widget =

# (list) List of Android permissions to add to the app
# android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (bool) Indicate if the app should be a fullscreen activity or not
# android.fullscreen = True

# (bool) Indicate if the app should be a window activity or not
# android.window = False

# (str) Use a specific Android log handler (default is 'python')
# android.log_handler = python

# (bool) Indicate if the app should use the python-for-android logging system
# android.use_p4a_logging = True

# (str) Additional arguments to pass to p4a
# android.extra_args = --enable-objc-arc

#
# iOS specific
#

# (str) iOS bundle identifier
# ios.bundle_identifier = %(package.domain)s.%(package.name)s

# (str) iOS version (format: X.Y.Z)
# ios.version = 1.0.0

# (bool) Enable iOS iCloud support
# ios.iCloud = False

# (list) List of iOS frameworks to add to the app
# ios.frameworks =

# (list) List of iOS plist entries to add to the app
# ios.plist_entries =

# (str) iOS app icon (use a single image with size 1024x1024)
# ios.icon.filename = %(source.dir)s/data/icon.png

# (str) iOS presplash image (use a single image with size 1024x1024)
# ios.presplash.filename = %(source.dir)s/data/presplash.png

# (bool) Enable iOS specific compilation (just for the build process)
# ios.codesign = False

# (bool) Enable iOS entitlements
# ios.entitlements = False

#
# Buildozer global settings
#

# (str) Path to buildozer global directory (where the android platform is stored)
# buildozer_dir = ~/.buildozer

# (bool) Indicate if the buildozer cache should be preserved between runs
# buildozer_cache = True

# (bool) Indicate if the buildozer log should be verbose or not
# buildozer_verbose = 1

# (str) Path to the application directory (where the main.py is)
# app_dir = .

# (str) Path to the dist directory (where the apk is stored)
# dist_dir = bin

# (str) Path to the build directory (where the build process happens)
# build_dir = .buildozer

# (str) Path to the platform directory (where the android platform is stored)
# platform_dir = ~/.buildozer/android/platform

# (str) Path to the packages directory (where the recipes are stored)
# packages_dir = ~/.buildozer/android/packages

# (str) Path to the cache directory (where the downloads are stored)
# cache_dir = ~/.buildozer/cache

# (str) Path to the log directory (where the logs are stored)
# log_dir = ~/.buildozer/logs

#
# DEPRECATED: Do not use these anymore
#
# android.ndk_version =
# android.sdk_version =
