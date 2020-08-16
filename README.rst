R E A D M E


OKLIB is library that provides the basic for a console program.
OKLIB has been placed in the Public Domain and contains no copyright or LICENSE.

installation is through pypi:

 > sudo pip3 install oklib


you can also install from the tarball, see https://pypi.org/project/oklib/#files


U S A G E


OKLIB has it's own shell, you can run it by giving the ok command on the prompt, it will return with no response:

:: 

 $ ok
 $ 

you can use oksh <cmd> to run a command directly:

::

 $ ok cmds
 cfg|cmd|cor|dne|edt|eml|flt|fnd|krn|log|mbx|tdo|tsk|upt|ver|wd

using the -s option starts a shell:

::

 $ ok -s
 > cmds
 cfg|cmd|cor|dne|edt|eml|flt|fnd|krn|log|mbx|tdo|tsk|upt|ver|wd
 >


OKLIB can load user defined modules from a "mods" directory in it's working
directory, you can put your own modules overthere, default working directory
is ~/.ok

if you run ob as root it will use /var/lib/ok/mods/ as the modules directory.


M O D U L E S


OLIB has the following modules:

::

    clk		- clock
    csl		- console
    obj 	- objects
    hdl		- handler
    prs 	- parser


P R O G R A M M I N G


installing from the github repository is also possible:

 > git clone http://github.com/bthate/oklib


commands look like this:

::

 def command(event):
     event.reply("ok")


H A V E   F U N 


enjoy the coding ! ;]


C O N T A C T


Bart Thate

bthate@dds.nl | botfather #dunkbots irc.freenode.net | https://pypi.org/project/olib
