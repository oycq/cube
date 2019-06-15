https://docs.odriverobotics.com/ #odrive site

git clone https://github.com/oycq/cube

sudo apt-get install python3-pip

sudo pip3 install odrive

sudo pip3 install opencv-python \
#if error, Do NOT use pip source

echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="0d[0-9][0-9]", MODE="0666"' | sudo tee /etc/udev/rules.d/91-odrive.rules
 
sudo udevadm control --reload-rules

sudo udevadm trigger

#use command bellow to test odrive
odrivetool 

sudo apt-get install python3-tk

sudo chmod +666 <your-port>
