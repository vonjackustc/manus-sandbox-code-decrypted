#!/bin/bash

export HOME=/home/ubuntu
source ~/.bashrc
export DISPLAY=:0
export QT_QPA_PLATFORM=wayland
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1

EXTENSION_HOME=/opt/.manus/.packages/chrome-extensions
# EXTENSION_HOME=/home/ubuntu/extensions/

EXTENSIONS=${EXTENSION_HOME}/ublock-origin,${EXTENSION_HOME}/manus-helper
# EXTENSIONS=${EXTENSION_HOME}/manus-helper

google-chrome \
    --disable-field-trial-config \
    --disable-background-networking \
    --enable-features=NetworkService,NetworkServiceInProcess \
    --disable-background-timer-throttling \
    --disable-backgrounding-occluded-windows \
    --disable-back-forward-cache \
    --disable-breakpad \
    --disable-client-side-phishing-detection \
    --disable-component-extensions-with-background-pages \
    --disable-component-update \
    --no-default-browser-check \
    --disable-default-apps \
    --disable-dev-shm-usage \
    --disable-features=ImprovedCookieControls,LazyFrameLoading,GlobalMediaControls,DestroyProfileOnBrowserClose,MediaRouter,DialMediaRouteProvider,AcceptCHFrame,AutoExpandDetailsElement,CertificateTransparencyComponentUpdater,AvoidUnnecessaryBeforeUnloadCheckSync,Translate,HttpsUpgrades,PaintHolding \
    --allow-pre-commit-input \
    --disable-hang-monitor \
    --disable-ipc-flooding-protection \
    --disable-popup-blocking \
    --disable-prompt-on-repost \
    --disable-renderer-backgrounding \
    --force-color-profile=srgb \
    --metrics-recording-only \
    --no-first-run \
    --password-store=basic \
    --use-mock-keychain \
    --no-service-autorun \
    --export-tagged-pdf \
    --disable-search-engine-choice-screen \
    --mute-audio \
    --blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4 \
    --use-angle=swiftshader-webgl \
    --noerrdialogs \
    --window-size=1280,1029 \
    --window-position=0,0 \
    --no-sandbox \
    --lang=en-US \
    --num-raster-threads=4 \
    --disable-gpu \
    --user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36' \
    --remote-debugging-port=9222 \
    --load-extension="${EXTENSIONS}" \
    --user-data-dir=/home/ubuntu/.browser_data_dir

# 一些选项说明
# --no-sandbox：https://monica.im/share/chat?shareId=9tEuQz3WEpfzvN4Z&copied=1

# 一些去掉了的选项，加上会有安全提示，没有明确收益的情况下先不加
    # --ozone-override-screen-size=1080,1080 \
    # --disable-blink-features=AutomationControlled \
    # --enable-automation \


# 加载多个插件可以用逗号隔开
# --load-extension="/path/to/a,/path/to/b"