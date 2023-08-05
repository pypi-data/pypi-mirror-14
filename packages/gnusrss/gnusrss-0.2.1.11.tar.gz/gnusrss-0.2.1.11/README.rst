**Table of Contents**

-  `gnusrss <#gnusrss>`__

   -  `English <#english>`__

      -  `About <#about>`__
      -  `Features <#features>`__
      -  `Requirements <#requirements>`__
      -  `Git repository <#git-repository>`__
      -  `Install <#install>`__
      -  `Configuration <#configuration>`__
      -  `Crontab <#crontab>`__
      -  `Use with twitter2rss and/or GNU
         Social <#use-with-twitter2rss-andor-gnu-social>`__
      -  `License <#license>`__

   -  `Castellano <#castellano>`__

      -  `Acerca de <#acerca-de>`__
      -  `Features <#features>`__
      -  `Requisitos <#requisitos>`__
      -  `Repositorio git <#repositorio-git>`__
      -  `Instalación <#instalacin>`__
      -  `Configuración <#configuracin>`__
      -  `Crontab <#crontab>`__
      -  `Uso con twitter2rss y/o GNU
         Social <#uso-con-twitter2rss-yo-gnu-social>`__
      -  `Licencia <#licencia>`__

gnusrss
=======

English
-------

About
~~~~~

gnusrss parse feeds and post them to GNU Social. The idea of ​​this
program came from `spigot <https://github.com/nathans/spigot>`__, a
program that posts feeds to the social network
`pump.io <https://pump.io>`__ as does gnusrss but better, because it
controls the possible flood. gnusrss does not have this option and it
will be managed with the crontab (for now).

Features
~~~~~~~~

-  Multiple feed and GNU Social accounts support
-  sqlite3 is used to store the feeds
-  Can fetch RSS files or url indistinctly
-  Twitter image upload support when used with
   `twitter2rss <http://daemons.cf/cgit/twitter2rss>`__

Requirements
~~~~~~~~~~~~

Need a version equal to or greater than python 3 and some libraries:

-  `feedparser <//pypi.python.org/pypi/feedparser>`__ >= 5.0
-  `pycurl <//pypi.python.org/pypi/pycurl/>`__ >= 7.0

Git repository
~~~~~~~~~~~~~~

It's in two places:

-  http://daemons.cf/cgit/gnusrss: the original repository
-  https://notabug.org/drymer/gnusrss/: A mirror in which it can be put
   issues and feature requests

Install
~~~~~~~

As with any program that uses python, it should be used a virtual
environment (virtualenv), but that is user selectable. It's possible to
use one of the next installation methods:

Install via pip:

::

    $ su -c "pip3 install gnusrss"

Clone the repository:

::

    $ git clone git://daemons.cf/gnusrss
    # OR ...
    $ git clone https://notabug.org/drymer/gnusrss/
    $ cd gnusrss
    $ su -c "pip3 install -r requirements.txt"
    $ su -c "python3 setup.py install"

If on parabola:

::

    $ su -c "pacman -S gnusrss"

Configuration
~~~~~~~~~~~~~

The program is (or should be) quite intuitive. Running the following,
should show the basics:

::

    $ gnusrss.py
    usage: gnusrss [-h] [-c file_name] [-C] [-p config_file] [-P] [-k file_name]

    Post feeds to GNU Social

    optional arguments:
        -h, --help            show this help message and exit
        -c file_name, --create-config file_name
                        creates a config file
        -C, --create-db       creates the database
        -p config_file, --post config_file
                        posts feeds
        -P, --post-all        posts all feeds
        -k file_name, --populate-database file_name
                        fetch the RSS and save it in the database

In any case, if not clear, read the following.

For the first use, it must be created the database and the first
configuration file. This can done using the same command, like this:

::

    $ gnusrss.py --create-db --create-config daemons

Then it will ask several questions to create the first configuration
file. It should look like this:

::

    Database created!
    Hi! Now we'll create config file!
    Please enter the feed's URL: https://daemons.cf/rss.xml
    Please enter your username (user@server.com): drymer@quitter.se
    Please enter your password: falsePassword
    Do you need to shorten the URLs that you 'post? Please take in account
    That You should only use it if your node only have 140 characters.
    Answer with "yes" or just press enter if you do not want to use it:
    Please enter your feed's fallbackurl. If you do not want or have one,
    just press enter:
    Now we're gona fetch the feed. Please wait ...
    Done! The tags are:
       tags
       title_detail
       link
       authors
       links
       author_detail
       published_parsed
       title
       summary
       id
       author
       published
       guidislink
       summary_detail
    The XML has-been parsed. Choose wich format you want:
    Please put the tags inside the square brackets
    Ex: {title} - {link} by @{author}: {title} - {link} by @{author}

The file is saved under the name 'daemons.ini'. It should look like
this:

::

    [Feeds]
    feed = https://daemons.cf/rss.xml
    user = drymer@quitter.se
    password = falsePassword
    shorten =
    fallback_feed =
    format = {title} - {link} by @ {author}

It can create all the configuration files you want. When creating the
above file, it put into the database all the feeds that had so far.
Thus, when running **gnusrss** for the first time, it will not post
nothing to GNU Social until the feed has new information. To post feeds
from a concrete config file or all execute, respectively, the following:

::

    $ gnusrss.py -p daemons.ini
    $ gnusrss.py -P

If the config file is created manually and the user don't want to post
all the feed's content, just use the –populate-database option to save
them to the database:

::

    $ gnusrss.py -k otherFile.ini

Crontab
~~~~~~~

The recommended way to execute **gnurss** is using the crontab. Each
time it's run, a single item of the feed will be posted to prevent
flood. Depending on the number of feeds that are published, you should
choose a different runtime. For a blog that publishs once a day, it
could be used the following:

::

    * 12 * * * cd $rutaDEgnusrss && gnusrss.py -p daemons.ini

So it runs once, every day at midday. If, however, it's used with
`twitter2rss <http://daemons.cf/cgit/twitter2rss/>`__, it could be
recommended putting it to run every five minutes. It has to be
remembered that is important to run in the directory where the database
was created, because is where it will search it..

Use with twitter2rss and/or GNU Social
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It works like any feed, except for the field that is published. In both
you have to choose ``{summary}``. An example configuration file is as
follows:

::

    [feeds]
    feed = https://quitter.se/api/statuses/user_timeline/127168.atom
    user = drymer@quitter.se
    password = falsePassword
    shorten =
    fallback_feed =
    format = {summary}

The feed can be achieved by looking at the source code of the page of
the account you want. For
`twitter2rss <http://daemons.cf/cgit/twitter2rss>`__, you can host it or
can use this `web <http://daemons.cf/twitter2rss>`__.

License
~~~~~~~

::

    This program is free software: you can redistribute it and / or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, Either version 3 of the License, or
    (At your option) any later version.

    This program is distributed in the hope That it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    Along With This Program. If not, see <http://www.gnu.org/licenses/>.

Castellano
----------

Acerca de
~~~~~~~~~

gnusrss parsea feeds y los postea en GNU Social. La idea de hacer este
programa surgió de `spigot <https://github.com/nathans/spigot>`__, un
programa que postea feeds en la red social `pump.io <https://pump.io>`__
igual que hace gnusrss pero mejor, ya que controla el posible flood.
gnusrss no tiene esta opción y se controlará con el propio crontab (de
momento).

Features
~~~~~~~~

-  Soporta múltiples feeds y cuentas de GNU Social
-  sqlite3 es usado para guardar los feeds
-  Se puede usar tanto archivos RSS cómo url indistintamente
-  Soporta la súbida de imágenes de Twitter cuando es usado en conjunto
   con `twitter2rss <http://daemons.cf/cgit/twitter2rss>`__

Requisitos
~~~~~~~~~~

Necesita una versión de python igual o superior a la 3 y algunas
librerias:

-  `feedparser <https://pypi.python.org/pypi/feedparser>`__ >= 5.0
-  `pycurl <https://pypi.python.org/pypi/pycurl/>`__ >= 7.0

Repositorio git
~~~~~~~~~~~~~~~

Está en dos sitios:

-  http://daemons.cf/cgit/gnusrss: el repositorio original
-  https://notabug.org/drymer/gnusrss/: un mirror, en el que se pueden
   poner los problemas y sugerencias de mejoras

Instalación
~~~~~~~~~~~

Cómo con cualquier programa con python, es recomendable usar un entorno
virtual (virtualenv), pero eso queda a elección del usuario. Se puede
escoger entre los siguientes metodos:

Instalar usando pip:

::

    $ su -c "pip3 install gnusrss"

Clonar el repositorio:

::

    $ git clone git://daemons.cf/gnusrss
    # O ...
    $ git clone https://notabug.org/drymer/gnusrss/
    $ cd gnusrss
    $ su -c "pip3 install -r requirements.txt"
    $ su -c "python3 setup.py install"

Si se usa parabola:

::

    $ su -c "pacman -S gnusrss"

Configuración
~~~~~~~~~~~~~

El programa es (o debería ser) bastante intuitivo. Ejecutando lo
siguiente, deberia verse lo básico:

::

    $ gnusrss.py
    usage: gnusrss [-h] [-c file_name] [-C] [-p config_file] [-P] [-k file_name]

    Post feeds to GNU Social

    optional arguments:
        -h, --help            show this help message and exit
        -c file_name, --create-config file_name
                        creates a config file
        -C, --create-db       creates the database
        -p config_file, --post config_file
                        posts feeds
        -P, --post-all        posts all feeds
        -k file_name, --populate-database file_name
                        fetch the RSS and save it in the database

En cualquier caso, si no queda claro, leer lo siguiente.

Para el primer uso, la base de datos y el primer archivo de
configuración deben ser creados. Podemos hacerlo usando la misma orden,
tal que así:

::

    $ gnusrss.py --create-db --create-config daemons

A continuación hará varias preguntas para configurar el primer archivo
de configuración. Debería verse así:

::

    Database created!
    Hi! Now we'll create de config file!
    Please introduce the feed's url: https://daemons.cf/rss.xml
    Please introduce your username (user@server.com): drymer@quitter.se
    Please introduce your password: contraseñaFalsa
    Do you need to shorten the urls that you post? Please take in account
    that you should only use it if your node only has 140 characters.
    Answer with "yes" or just press enter if you don't want to use it:
    Please introduce your feed's fallbackurl. If you don't want or have one,
    just press enter:
    Now we're gona fetch the feed. Please wait...
    Done! The tags are:
       tags
       title_detail
       link
       authors
       links
       author_detail
       published_parsed
       title
       summary
       id
       author
       published
       guidislink
       summary_detail
    The XML has been parsed. Choose wich format you want:
    Please put the tags inside the square brackets
    Ex: {title} - {link} by @{author}: {title} - {link} by @{author}

El archivo se guardará con el nombre 'daemons.ini'. Después de todas
estas preguntas, debería verse similar a esto:

::

    [feeds]
    feed = https://daemons.cf/rss.xml
    user = drymer@quitter.se
    password = contraseñaFalsa
    shorten =
    fallback_feed =
    format = {title} - {link} by @{author}

Se pueden crear todos los archivos de configuración que se quieran. Al
haber creado el archivo anterior, se han metido en la base de datos
todos los feeds que habian hasta el momento. Por lo tanto, cuando se
ejecuta **gnusrss** por primera vez, no posteará nada en GNU Social, a
menos que el feed tenga nueva información. Para postear los feeds de un
archivo o todos, ejecutar, respectivamente, lo siguiente:

::

    $ gnusrss.py -p daemons.ini
    $ gnusrss.py -P

Si el archivo de configuración ha sido creado manualmente y no se quiere
postear el contenido del feed, sólo hay que ejecutar la opción
–populate-database para guardar estos en la base de datos:

::

    $ gnusrss.py -k otherFile.ini

Crontab
~~~~~~~

El modo recomendado de ejecución de gnusrss es usando el crontab. Cada
vez que se ejecute posteará un sólo elemento del feed para evitar el
flood. Según la cantidad de feeds que se publiquen, se deberia escoger
un tiempo de ejecución distinto. Para un blog que publique una vez al
día, con poner lo siguiente, deberia valer:

::

    * 12 * * * cd $rutaDEgnusrss && gnusrss.py -p daemons.cf

Así se ejecuta una vez al día, a las doce de la mañana. Si, en cambio,
lo usasemos con `twitter2rss <http://daemons.cf/cgit/twitter2rss/>`__,
se recomienda poner que se ejecute cada cinco minutos. Hay que recordar
que es importante que se ejecute en el directorio en el que se ha creado
la base de datos, ya que es ahí dónde la buscará.

Uso con twitter2rss y/o GNU Social
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Funciona igual que con cualquier feed, exceptuando el campo que se
publica. En ambos hay que escoger ``{summary}``. Un ejemplo de archivo
de configuración sería el siguiente:

::

    [feeds]
    feed = https://quitter.se/api/statuses/user_timeline/127168.atom
    user = drymer@quitter.se
    password = contraseñaFalsa
    shorten =
    fallback_feed =
    format = {summary}

El feed se puede conseguir mirando el código fuente de la página de la
cuenta que se quiere. En el caso de
`twitter2rss <http://daemons.cf/cgit/twitter2rss>`__, se puede hostear o
se puede usar esta `web <http://daemons.cf/twitter2rss>`__.

Licencia
~~~~~~~~

::

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

