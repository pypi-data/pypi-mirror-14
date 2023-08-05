.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

=======================================================
Mercurial Keyring
=======================================================

Mercurial Keyring is a Mercurial_ extension used to securely save HTTP
and SMTP authentication passwords in password databases (Gnome
Keyring, KDE KWallet, OSXKeyChain, Windows Vault etc).

With ``mercurial_keyring`` active, Mercurial remembers your passwords
and reuses them without prompting (as if you stored them in ``.hgrc``),
but password storage is reasonably secure.

Actual password storage is implemented by the keyring_ library, this 
extension glues it to Mercurial.

.. contents::
   :local:
   :depth: 2

.. sectnum::

.. _keyring: http://pypi.python.org/pypi/keyring
.. _Mercurial: http://mercurial.selenic.com

How does it work
=======================================================

On your first pull or push to HTTP url (or first email sent via given
SMTP server), you are prompted for the password, just like bare
Mercurial does. But the password you entered is saved to appropriate
password database. On successive runs, whenever the password is
needed, ``mercurial_keyring`` checks for password in password
database, and uses it without troubling you.

In case password turns out to be incorrect (for example, because you
changed it, or entered it incorrectly), ``mercurial_keyring`` prompts
you again, and overwrites the password.

You can use many passwords (for various remote urls).  Saved passwords
are identified by pair of username and url prefix. See below for
information how to configure those properly.

Installation
=======================================================

Prerequisites
-------------

This extension requires keyring_ and `mercurial_extension_utils`_ to
work. In many cases both will be installed automatically while you
install ``mercurial_keyring``, but you may need to control the process.

The keyring_ library can usually be installed by::

    pip install --user keyring

(or ``easy_install keyring``), but on some systems it is preferable to
use official distribution archive. For example, on Debian and Ubuntu,
you may install ``python-keyring`` and either ``python-keyring-gnome``
or ``python-keyring-kwallet`` packages::

    sudo apt-get install python-keyring python-keyring-gnome

(this will save you the need to provide working compiler and various
development libraries).

The `mercurial_extension_utils`_ module is tiny Python-only module,
which can be installed by::

    pip install --user mercurial_extension_utils

but in some cases (Windows…) requires more care. See
`mercurial_extension_utils`_ documentation.
    

Extension installation
----------------------

There are two possible ways of installing the extension: using PyPi package,
or using source clone.

To install as a package::

    pip install --user mercurial_keyring

(or ``sudo pip install mercurial_keyring`` for system-wide
installation) and then enable it in ``~/.hgrc`` (or
``/etc/mercurial/hgrc`` or ``Mercurial.ini``) using::

    [extensions]
    mercurial_keyring = 

To install using source clone, install keyring_ according to the
instructions above, then clone::
    
    hg clone https://bitbucket.org/Mekk/mercurial_keyring/
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/

and configure Mercurial using  full path to the extension module::

    [extensions]
    mercurial_keyring = /path/to/mercurial_keyring/mercurial_keyring.py

.. _the code: 
.. _mercurial_keyring.py: http://bitbucket.org/Mekk/mercurial_keyring/src/tip/mercurial_keyring.py

Password backend configuration
=======================================================

The most appropriate password backend should usually be picked without
configuration (considering installed libraries, operating system,
active desktop session). Still, if necessary, it can be configured
using ``keyringrc.cfg`` file.  Refer to keyring_ docs for more
details.

.. note::

   With current (as I write) keyring (5.6), this file is (on Linux)
   located at ``~/.local/share/python_keyring/keyringrc.cfg`` and
   it's example content looks like::

        [backend]
        default-keyring=keyring.backends.Gnome.Keyring
        # default-keyring=keyring.backends.kwallet.Keyring

   For list of known backends run ``pydoc keyring.backends``.


``hgrc`` configuration (HTTP)
=======================================================

Mercurial Keyring uses standard Mercurial ``[auth]`` configuration to
detect your username (on given remote) and url prefix. You are
strongly advised to configure both.

Without the username ``mercurial_keyring`` can't save or restore
passwords, so it disables itself.

Without url prefix ``mercurial_keyring`` works, but binds passwords to
repository urls. That means you will have to (re)enter password for
every repository cloned from given remote (and that there will be many
copies of this password in secure storage).

Repository level configuration
------------------------------------

Edit repository-local ``.hg/hgrc`` and save there the remote
repository path and the username, but do not save the password. For
example:

::

    [paths]
    myremote = https://my.server.com/hgrepo/someproject

    [auth]
    myremote.prefix = https://my.server.com/hgrepo
    myremote.username = John

Simpler form with url-embedded name can also be used:

::

    [paths]
    bitbucket = https://John@my.server.com/hgrepo/someproject/

but is not recommended.

Note that all repositories sharing the same ``prefix`` share the same
password.

Mercurial allows also for password in ``.hg/hgrc`` (either given by
``«prefix».password``, or embedded in url). If such password is found,
Mercurial Keyring disables itself.


Account-level configuration
---------------------------

If you are consistent about remote repository nicknames, you can
configure the username in your `~/.hgrc` (`.hgrc` in your home
directory). For example, write there::

    [auth]
    acme.prefix = hg.acme.com/repositories
    acme.username = johnny
    acme.schemes = http https
    bitbucket.prefix = https://bitbucket.org
    bitbucket.username = Mekk
    mydep.prefix = https://dev.acmeorg.com
    mydep.username = drmartin

and as long as you use  ``acme`` alias for repositories like
``https://hg.acme.com/repositories/my_beautiful_app``, username
``johnny`` will be used, and the same password reused. Similarly
any ``hg push bitbucket`` will share the same password.

With such config repository-level ``.hg/hgrc`` need only contain
``[paths]``.

Additional advantage of this method is that it works also during
`clone`.


.. note::

   Mercurial Keyring works well with `Path Pattern`_. On my setup I use
   prefix as above, and::

       [path_pattern]
       bitbucket.local = ~/devel/{below}
       bitbucket.remote = https://bitbucket.org/Mekk/{below:/=-}
 
   so all my repositories understand ``hg push bitbucket`` without
   any repository-level configuration.


``hgrc`` configuration (SMTP)
=======================================================

Edit either repository-local ``.hg/hgrc``, or ``~/.hgrc`` and set
there all standard email and smtp properties, including SMTP
username, but without SMTP password. For example:

::

    [email]
    method = smtp
    from = Joe Doe <Joe.Doe@remote.com>

    [smtp]
    host = smtp.gmail.com
    port = 587
    username = JoeDoe@gmail.com
    tls = true

Just as in case of HTTP, you *must* set username, but *must not* set
password here to use the extension, in other cases it will revert to
the default behavior.

Usage
======================================================

Saving and restoring passwords
-------------------------------------------------------

Configure the repository as above, then just ``hg pull``, ``hg push``,
etc.  You should be asked for the password only once (per every
username and remote repository prefix or url combination).

Similarly, for email, configure as above and just ``hg email``.
Again, you will be asked for the password once (per every username and
email server address combination).

Checking password status (``hg keyring_check``)
-------------------------------------------------------

The ``keyring_check`` command can be used to check whether/which
password(s) are saved. It can be used in three ways:

- without parameters, it prints info related to all HTTP paths
  defined for current repository (everything from ``hg paths``
  that resolves to HTTP url)::

    hg keyring_check

- given alias as param, it prints info about this alias::

    hg keyring_check work

- finally, any path can be checked::

    hg keyring_check https://bitbucket.org/Mekk/mercurial_keyring

Deleting saved password (``hg keyring_clear``)
-------------------------------------------------------

The ``keyring_clear`` command removes saved password related to given
path. It can be used in two ways:

- given alias as param, it drops password used by this alias::

    hg keyring_clear work

- given full path, it drops password related to this path::

    hg keyring_clear https://bitbucket.org/Mekk/mercurial_keyring

Managing passwords using GUI tools
------------------------------------------------------

Many password backends provide GUI tools for password management,
for example Gnome Keyring passwords can be managed using ``seahorse``,
and KDE Wallet using ``kwalletmanager``. Those GUI tools can be used
to review, edit, or delete saved passwords.

Unfortunately, as I write, keyring_ library does not allow one to
configure how/where exactly saved passwords are put in the hierarchy,
and the place is not always intuitive. For example, in KDE Wallet, all
passwords saved using ``mercurial_keyring`` show up in the folder
named ``Python``.

.. note::

   This is slightly problematic in case ``mercurial_keyring`` is not
   the only program using keyring_ library. Passwords saved by another
   Python application or script (which also uses keyring_) will be put
   into the same place, and it may be unclear which password belongs
   to which program. To remedy this, ``mercurial_keyring`` applies
   slightly unusual labels of the form
   ``«username»﻿@@﻿«urlprefix»﻿@﻿Mercurial`` - for example my bitbucket
   password is labelled ``Mekk﻿@@﻿https﻿://﻿bitbucket.org﻿@﻿Mercurial``.

Implementation details
=======================================================

The extension is monkey-patching the mercurial ``passwordmgr`` class
to replace the ``find_user_password`` method. Detailed order of operations
is described in the comments inside `the code`_.

History
=======================================================

See `HISTORY.txt`_.

Development
=======================================================

Development is tracked on BitBucket, see 
http://bitbucket.org/Mekk/mercurial_keyring/


Additional notes
=======================================================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/KeyringExtension

Check also `other Mercurial extensions I wrote`_.

.. _other Mercurial extensions I wrote: http://mekk.bitbucket.org/mercurial.html

.. _HISTORY.txt: http://bitbucket.org/Mekk/mercurial_keyring/src/tip/HISTORY.txt
.. _TortoiseHg: http://tortoisehg.bitbucket.org/
.. _Mercurial: http://mercurial.selenic.com
.. _mercurial_extension_utils: https://bitbucket.org/Mekk/mercurial-extension_utils/
.. _Path Pattern: https://bitbucket.org/Mekk/mercurial-path_pattern/
