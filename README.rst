README
######

Welcome to OKBOT,

OKBOT is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. It installs itself as a service so
you can get it restarted on reboot. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it, have it log objects on
disk and search. 

OKBOT is placed in the Public Domain, no COPYRIGHT, no LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install oklib

SERVICE
=======

If you want to run the bot 24/7 you can install OPBOT as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/ok.service file, enable it and call restart:

::

 $ sudo cp okbot.service /etc/systemd/system
 $ sudo systemctl enable okbot
 $ sudo systemctl daemon-reload
 $ sudo systemctl start okbot

default channel/server to join is #okbot on localhost.

to configure  use the cfg command:

::

 $ sudo okctl cfg server=<server> channel=<channel> nick=<nick>

add your userhost to the bot by introducing yourself as a user:

::

 $ sudo okctl met <userhost>

the bot should now listen to the !cmd typed.

if you don't want okbot to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/okbot.service

OPCTL
=====

OPBOT has it's own CLI, the okctl program. It needs root because the okbot
program uses systemd to get it started after a reboot. You can run it on 
the shell prompt and, as default, it won't do anything.

:: 

 $ sudo okctl
 $ 

you can use okctl <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ sudo okctl cmd
 cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver


IRC
===

configuration is done with the cfg command:

::

 $ sudo okctl cfg
 channel=#okbot nick=okbot port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ sudo okctl cfg server=irc.freenode.net channel=\#dunkbots nick=okbot
 ok

add you irc client's userhost to the bot:

::

 $ sudo okctl met ~botfather@jsonbot/daddy
 ok

then restart the okbot service:

::

 $ sudo systemctl restart okbot

the bot should listen to your commands now, try !cmd.

RSS
===

OPBOT provides with the use of feedparser the possibility to server rss
feeds in your channel. OPBOT runs with no dependancies and feedparser needs
to be installed to have rss feeds working:

::

 $ sudo apt install python3-feedparser

to add an url use the rss command with an url:

::

 $ sudo okctl rss https://github.com/bthate/okbot/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ sudo okctl fnd rss
 0 https://github.com/bthate/okbot/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ sudo okctl ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller.

::

 $ sudo bot mods=irc,rss

UDP
===

OPBOT also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

adding the udp to mods= load the udp to irc gateway

::

 $ sudo okbot mods=irc,udp

use the 'okudp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | okudp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to OPBOT, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to OPBOT in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

OPBOT provides the following modules:

::

    ok.cli		- cli commands
    ok.cmd		- list of commands
    ok.clk              - clock/repeater
    ok.dbs              - databases
    ok.ent		- log and todo
    ok.fnd		- locate objects
    ok.hdl              - handler
    ok.irc		- internet relay chat
    ok.itr              - introspection
    ok.obj              - objects
    ok.prs              - parser
    ok.rss		- Rich Site Syndicate
    ok.run              - runtime
    ok.sys		- system commands
    ok.tbl              - tables
    ok.thr              - threads
    ok.trm              - terminal
    ok.udp		- Uniform Datagram Protocol
    ok.utl              - utilities
    ok.usr		- users
    ok.ver		- version

CONTACT
=======

"contributed back to society"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots at irc.freenode.net
