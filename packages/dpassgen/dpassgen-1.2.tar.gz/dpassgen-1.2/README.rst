dpassgen:  Generate random word-based password
##############################################

:author:  John H. Dulaney <jdulaney@fedoraproject.org>

Based on the idea from https://xkcd.com/936/, uses /dev/urandom to
pick a number of words from /usr/share/dict/words or
/usr/dict/words.

Installation
------------

  sudo python setup.py install

or

  python3 setup.py install


Usage:
------

  dpassgen <number>

where <number> is the number of words you would like in your password.