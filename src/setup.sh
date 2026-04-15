sudo apt install -y libcap-dev libcamera-dev python3-libcamera python3-venv python3-pip libkms++-dev libdrm-dev libcamera-tools
python3 -m venv --system-site-packages venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

sudo cp config.txt /boot/firmware/config.txt
sed "s/\[USER\]/$(whoami)/g" 99-wro.rules | sudo tee /etc/udev/rules.d/99-wro.rules

sudo usermod -aG video,gpio $(whoami)