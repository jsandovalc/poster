# Poster app for multiple social networks.

    This is the source code of poster
    Jonathan Sandoval <jsandoval@utp.edu.co>

## Tasks
1. Post to facebook from python/cyclone.
2. Post to facebook group from python/cyclone.
3. Schedule post.
4. Schedule multiple posts.
5. Create web UI for posting a single post.
6. Post to multiple walls/groups.
7. Update UI to suppor multiple posting.


## About

This file has been created automatically by cyclone for poster.
It contains the following:

- ``scripts/``: other useful scripts


### Running

For development and testing:

    gem install foreman
    cd poster
    foreman start

For production on any foreman based env:

    Follow foreman instructions, configure Procman as needed.
    Check the .env file and the configuration file for your app.

For production at heroku:

    - Start a git repo
        git init
        git add .
        git commit -m 'first'
        heroku create poster # (or whatever name you want)
        heroku push heroku master
    - check your app, make it better, create a db, etc


## Customization

This section is dedicated to explaining how to customize your brand new
package.


### Databases

cyclone provides built-in support for SQLite and Redis databases.
It also supports any RDBM supported by the ``twisted.enterprise.adbapi``
module, like MySQL or PostgreSQL.

The default configuration file ``poster.conf`` ships with pre-configured
settings for SQLite, Redis and MySQL.

The code for loading all the database settings is in ``poster/config.py``.
Feel free to comment or even remove such code, and configuration entries. It
shouldn't break the web server.

Take a look at ``poster/utils.py``, which is where persistent database
connections are initialized.


### Internationalization

cyclone uses the standard ``gettext`` library for dealing with string
translation.

Make sure you have the ``gettext`` package installed. If you don't, you won't
be able to translate your software.

For installing the ``gettext`` package on Debian and Ubuntu systems, do this:

    apt-get install gettext

For Mac OS X, I'd suggest using [HomeBrew](http://mxcl.github.com/homebrew>).
If you already use HomeBrew, run:

    brew install gettext
    brew link gettext

For generating translatable files for HTML and Python code of your software,
run this:

    cat frontend/template/*.html poster/*.py | python scripts/localefix.py | xgettext - --language=Python --from-code=utf-8 --keyword=_:1,2 -d poster

Then translate poster.po, compile and copy to the appropriate locale
directory:

    (pt_BR is used as example here)
    vi poster.po
    mkdir -p frontend/locale/pt_BR/LC_MESSAGES/
    msgfmt poster.po -o frontend/locale/pt_BR/LC_MESSAGES/poster.mo

There are sample translations for both Spanish and Portuguese in this package,
already compiled.


### Cookie Secret

The current cookie secret key in ``poster.conf`` was generated during the
creation of this package. However, if you need a new one, you may run the
``scripts/cookie_secret.py`` script to generate a random key.

## Credits

- [cyclone](http://github.com/fiorix/cyclone) web server.
