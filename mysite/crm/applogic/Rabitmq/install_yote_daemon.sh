cp -r YoteService /usr/local
cp startyoteservice.sh /usr/local
cd /usr/local
chmod +x YoteService
chmod +x startyoteservice.sh
echo '/usr/local/startyoteservice.sh' >/etc/profile.d/yotestartserver.sh
chmod +x /etc/profile.d/yotestartserver.sh

