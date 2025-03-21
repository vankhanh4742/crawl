#!/bin/bash
set -e

# Cập nhật danh sách gói và cài đặt các công cụ cần thiết
sudo apt-get update
sudo apt-get install -y wget unzip

# Cài đặt Google Chrome nếu chưa có (phiên bản stable)
if ! command -v google-chrome &> /dev/null; then
    echo "Cài đặt Google Chrome..."
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
else
    echo "Google Chrome đã được cài đặt."
fi

# Lấy phiên bản chính của Chrome
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
echo "Phiên bản chính của Chrome: $CHROME_VERSION"

# Tải xuống phiên bản Chromedriver tương ứng với Chrome
LATEST_DRIVER=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")
echo "Phiên bản Chromedriver cần cài: ${LATEST_DRIVER}"

wget -N "https://chromedriver.storage.googleapis.com/${LATEST_DRIVER}/chromedriver_linux64.zip" -P ~/
unzip -o ~/chromedriver_linux64.zip -d ~/
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
rm ~/chromedriver_linux64.zip

echo "Chromedriver đã được cài đặt thành công tại /usr/local/bin/chromedriver"
