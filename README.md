# cfsresd
Daemon that scrapes urgmsg.net for SAGRN pager messages and sends them to Pushover

python daemon#requirements


#to get working
add your user token to user_token in daemon.py
add your app token to app_token in daemon.py

under daemon.py set if your looking for CFS MFS or SES
below that set the other filters .e.g Salisbury
this will find anything related so INFO , RESPONSE, OFFICERS

now below that set filters you want to ignore e.g OFFICERS

so what will happen now is you will get Salisbury RESPONSE and INFO but not OFFICERS.

#TODO 
get working with PDW so you don't rely on the net.

make .INI file for app_token and user_token
allow multiple user_token 

make a better readme
