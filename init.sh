sudo apt install shadowsocks
pip3 install flask numpy
if [ ! -d /etc/shadowsocks ]
then
    mkdir /etc/shadowsocks
fi
./runbbr.sh
