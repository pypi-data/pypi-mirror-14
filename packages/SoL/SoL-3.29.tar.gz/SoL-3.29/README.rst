.. -*- coding: utf-8 -*-

======================
 Scarry On Lin{e|ux}³
======================

-------------------------------------------------------------
Powerful and complete solution to manage Carrom championships
-------------------------------------------------------------

This project contains some tools that make it easier the organization of a championship of
Carrom_ tournaments using a variant of the `Swiss system`__.

__ https://en.wikipedia.org/wiki/Swiss-system_tournament

The main component is a Pyramid_ application serving two distinct user interfaces:

1. A very light, HTML only, read only view of the whole database, where you can actually browse
   thru the clubs, championships, tourneys, players and ratings. You can see it in action on
   the public SoL instance at http://sol3.arstecnica.it/lit/.

2. A complete ExtJS_ based desktop-like application, that exposes all the functionalities
   described below__ in an easy to manage interface, that you can try out visiting
   http://sol3.arstecnica.it/.

.. attention:: SoL 3 **requires** Python 3.3 or higher, it does **not** work with Python 2

.. warning:: SoL 3.1+ **requires** SQLite 3.8 or higher

__ Goals_

.. _Carrom: http://en.wikipedia.org/wiki/Carrom
.. _Pyramid: http://www.pylonsproject.org/
.. _ExtJS: http://www.sencha.com/products/extjs/

.. contents:: :depth: 2


Goals
=====

These are the key points:

1. Multilingual application

   Scarry spoke only Italian, because the i18n mechanism in Delphi (and in general under
   Windows) sucks. Most of the code was written and commented in Italian too, and that made it
   very difficult to get foreign contributions

2. Multiuser

   There is a *super user* (named “admin” by default) that can do everything, in particular
   assign a *nickname* and a *password* to any player, who can then log in and manage her own
   tournaments, but can't change information owned by other users

3. Real database

   Scarry used Paradox tables, but we are in the third millennium, now: SoL uses a real, even
   if simple and light, SQL database under its skin

4. Easy to use

   The application is usually driven by computer-illiterated guys, so little to no surprises

5. Easy to deploy

   Gods know how many hours went in building f*cking installers with BDE goodies

6. Bring back the fun

   Programming in Python is just that, since the beginning


High level description
----------------------

The application implements the following features:

* basic tables editing, like adding a new player, opening a new championship, manually tweaking
  the scores, and so on;

* handle a single tourney

  a. compose a list of `competitors`: usually this is just a single player, but there are two
     people in doubles, or more (teams)

  b. set up the first round, made up of `matches`, each pairing two distinct `competitors`: if
     the tournament is associated with a `rating` this considers the Glicko2__ rate of each
     player, otherwise uses a random pairing; either way, the tournament secretary is able to
     manually change the combinations

  c. print the game sheets, where the player will write the scores

  d. possibly show a clock, to alert the end of the game

  e. insert the score of each match

  f. compute the new ranking

  g. print the current ranking

  h. possibly offer a way to withdraw some competitors, or to add a new competitor

  i. compute the next round

  j. repeat steps c. thru i. usually up to seven rounds

  k. possibly offer a way to go back, delete last round, correct a score and repeat

  l. recompute the ranking, assigning prizes

  m. update the `rating` the tournament is associated to

* handle a championship of tourneys

  * each tourney is associated to one championship

  * print the championship ranking

* data exchange, to import/export whole tourneys in a portable way

__ http://en.wikipedia.org/wiki/Glicko_rating_system


Installation and Setup
======================

The very first requirement to install an instance of SoL on your own machine is getting Python
3.5 or better\ [#]_. This step obviously depends on the operating system you are using: on most
GNU/Linux distributions it is already available\ [#]_, for example on Debian and derivatives
like Ubuntu the following command will do the task::

  $ apt-get install python3

If instead you are using M$-Windows, you should select the right installer from the downloads__
page on http://www.python.org/.

.. topic:: Non *pure Python* packages and Windows

   The most problematic thing on Windows is being able to install all the required packages:
   a few of them are actually written in ``C`` and there are chances that your particular
   combination of Python version and Windows version (32bit vs 64bit in particular) isn't
   supported by the respective authors.

   If the installation fails because a suitable package cannot be found, your only option
   (other than bugging me) is to install the needed development tools on your machine and
   retry the installation: the installer should be able to figure out the details and compile
   the modules.

   Since a couple of years Microsoft started to pay attention to the Python world, and actually
   released a trimmed down version of its development suites expressly to `compile Python 2
   extension modules`__, but nothing equivalent is available for Python 3 yet. Instead, you
   need to install the complete `Visual Studio` suite in particular, for Python 3.5, the
   `Visual Studio 2015 Community Edition`__.

Another recommended, although optional, add-on is the `DejaVu fonts`__ set, to support a rather
wide range of `glyphs`__ when producing the PDFs printouts. As usual, on GNU/Linux it's a
matter of executing the following command

::

  $ apt-get install fonts-dejavu

or equivalent for your distribution, while on M$-Windows you need to download__ them and
extract the archive in the right location which usually is ``C:\Windows\Fonts``.

__ http://www.python.org/downloads/windows/
__ https://www.microsoft.com/en-us/download/details.aspx?id=44266
__ http://www.visualstudio.com/downloads/
__ http://dejavu-fonts.org/wiki/Main_Page
__ https://en.wikipedia.org/wiki/Glyph
__ http://sourceforge.net/projects/dejavu/files/dejavu/2.35/dejavu-fonts-ttf-2.35.zip


Easiest way, SoLista
--------------------

The easiest way is using SoLista_, a buildout_ configuration that will perform most of the
needed steps with a few clicks: this is particularly indicated if you are *not* fluent with the
command line interface of your operating system.

Follow the hopefully clear enough steps in SoLista's `README`__.

.. _SoLista: https://bitbucket.org/lele/solista/
.. _buildout: http://www.buildout.org/en/latest/
__ https://bitbucket.org/lele/solista/src/master/README.rst


Pre-built Docker image
----------------------

.. note:: This is a work-in-progress facility: better documentation and helper tools are on the
          way! It targets brave souls willing to face a *bleeding edge* experience.

          Current state has been contributed by `Amar Sanakal`__, thank you!

Another option, if you have a 64bit computer, is to run the pre-built Docker_ image.

__ https://bitbucket.org/amar-sanakal/solista
.. _Docker: https://www.docker.com/

Requirements
~~~~~~~~~~~~

First of all, you must enable the *hardware virtualization* in the ``BIOS`` of your computer.

Then you can proceed to install the ``Docker Engine`` for your particular operating system
(that is, `GNU/Linux`__, `Windows`__ or `Mac OS X`__).

After you have tested the install in the ``Docker Quickstart terminal`` (for example as
depicted here__), run the following command in the same window::

  docker run -d -p 80:6996 --name sol amarsanakal/solista

This will start the software and is now accessible on port 80. You can access it as
``http://<ip-address>``.

The ``<ip-address>`` is the ip address of the docker machine running on your PC. This would
have been displayed to you when you launched the Docker Quickstart terminal. You can check it
anytime by running::

  docker-machine ls

the ip address is shown under the URL column. Use that without the port number shown there. See
https://docs.docker.com/machine/get-started/ for more details.

__ https://docs.docker.com/linux/
__ https://docs.docker.com/windows/
__ https://docs.docker.com/mac/
__ https://docs.docker.com/windows/step_three/

Roadmap
~~~~~~~

1. Integrate the image description into SoL itself
2. Figure out how to persist data within the docker container
3. Find a way to automate the steps above, ideally providing a single *shell script* or *batch
   file* to hide nasty details
4. Complete this section
5. Figure out how to build a new image on hub.docker.com tagged with the right version,
   whenever a new SoL release happens


The good old way
----------------

1. Install ``SoL`` using ``pip``::

    pip install SoL

   that will download the latest version of SoL from PyPI__ and all its dependencies as well

   __ https://pypi.python.org/pypi/SoL

2. Install ExtJS_ 4.2.1::

    python3 -m metapensiero.extjs.desktop

3. Create a standard config file::

    soladmin create-config config.ini

   and edit it as appropriate; you can also directly specify the name and the password of the
   *super user* (by default the name is ``admin`` and the password will be asked
   interactively)::

    soladmin create-config --admin differentone --password str4nge

4. Setup the database::

    soladmin initialize-db config.ini

5. Load official data::

    soladmin restore config.ini

6. Run the application server::

    pserve config.ini

7. Enjoy!
   ::

    firefox http://localhost:6996/

   or, for poor Window$ users or just because using Python makes you
   happier::

    python -m webbrowser http://localhost:6996/


Development
===========

The complete sources are available on Bitbucket__ and can be downloaded with the following
command::

    git clone https://bitbucket.org/lele/sol

After that, you can setup a development environment by executing the command::

    pip install -r requirements/development.txt

If you are a developer, you are encouraged to create your own `fork` of the software and
possibly open a `pull request`: I will happily merge your changes!

You can run the test suite with either

::

    make test

or

::

    python setup.py nosetests

__ https://bitbucket.org/lele/sol


I18N / L10N
-----------

Currently SoL is translated in English\ [#]_, French and Italian. If you know other languages
and want to contribute, the easiest way to create a new translation is to create an account on
the Weblate__ site and follow its `translators guide`__.

.. image:: https://hosted.weblate.org/widgets/sol/-/287x66-white.png
   :target: https://hosted.weblate.org/engage/sol/
   :alt: Translation status
   :align: center

Otherwise if like me you prefer using more traditional tools\ [#]_ you can extract a copy of
the sources and operate directly on the local catalogs under the directory ``src/sol/locale``.

To extract translatable messages use the following command::

    make update-catalogs

To check your work you must compile them with::

    make compile-catalogs

__ https://hosted.weblate.org/projects/sol/
__ http://docs.weblate.org/en/latest/user/index.html


Feedback and support
--------------------

If you run in troubles, or want to suggest something, or simply a desire of saying *“Thank
you”* raises up, feel free to contact me via email as ``lele at metapensiero dot it``.

Consider also joining the `dedicated mailing list`__ where you can get in contact with other
users of the application. There is also an `issues tracker`__ where you can open a new tickets
about bugs or enhancements.

__ https://groups.google.com/d/forum/sol-users
__ https://bitbucket.org/lele/sol/issues

-----

.. [#] As of this writing I'm using version 3.5.1 and I'd recommend using that, but SoL used to
       work great with Python 3.3 and Python 3.4 as well.

.. [#] In fact it may even be already installed!

.. [#] The are actually two distinct catalogs, to take into account US and UK variants.

.. [#] GNU Emacs comes to mind of course, but there are zillions of them: start looking at the
       `gettext page <http://en.wikipedia.org/wiki/Gettext>`_ on Wikipedia.
