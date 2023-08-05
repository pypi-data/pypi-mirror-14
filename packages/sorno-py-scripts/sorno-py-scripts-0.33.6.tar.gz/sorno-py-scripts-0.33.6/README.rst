sorno-py-scripts
================

My python scripts. `sorno` is just a brand name that I use for my stuff.
It's convenient to use that as a package name instead of the usual "org.xxx".

The source code of the whole project is in github:
https://github.com/hermantai/sorno-py-scripts

PyPI page: https://pypi.python.org/pypi/sorno-py-scripts

All scripts support the "-h" or the "--help" option for documentation of the
scripts. Often the documentation is in the __doc__ of the script, so take a
look at that as well.

All scripts are prefixed with "`sorno_`" to avoid polluting the Scripts folder
(in Windows, /usr/local/bin in \*nix) of python or other binaries when this
suite is installed.

This project also includes the `sorno` library.

Installation
--------------------
If you don't have Python installed, you first need to install it from
https://www.python.org/downloads/. You need a version at least 2.7 but lower
than 3.0.

For the following commands, add **sudo** in front of the commands if you are
getting permission error.

A Python package management system will make your life easier, so install pip
by::

    $ easy_install pip

If easy_install is not on your system, you can check how to install it in
https://pythonhosted.org/setuptools/easy_install.html#installing-easy-install.

Install with pip
~~~~~~~~~~~~~~~~
::

    $ pip install sorno_py_scripts  # note that the project name is in underscores, not dashes

Install with easy-install
~~~~~~~~~~~~~~~~~~~~~~~~~
::

    $ easy_install sorno_py_scripts  # note that the project name is in underscores, not dashes

Install from source
~~~~~~~~~~~~~~~~~~~
You can install sorno-py-scripts from the source code by cloning the git repo::

    $ git clone https://github.com/hermantai/sorno-py-scripts

Then cd to the sorno-py-scripts directory::

    $ cd sorno-py-scripts

Install it::

    $ python setup.py install


Running the scripts
-------------------
Your scripts should be installed at your $PATH. For *nix system, they are
usually in */usr/local/bin*. For windows, they should be in a *Scripts*
directory under the Python installation.

Make sure your scripts are in the PATH system environment variables.

Then you can run the scripts by simply invoking them from the command line
console ($ is the prompt of the console)::

  $ sorno_gtasks.py -h

Running the tests
-----------------
In the directory containing the ./test.sh file, then run it::

    $ ./test.sh

You can run tests only for the sorno library::

    $ ./test_sorno.sh

Or tests only for the scripts::

    $ ./test_scripts.sh

Contents
--------------------
Use -h or --help options for the scripts to get more detail documentation for
each script.

sorno_alarm.py (alpha)
~~~~~~~~~~~~~~~~~~~~~~
A console alarm which uses the system bell as the alarm bell by default. You
set how
many seconds before the alarm goes off, not an absolute time in the future.
After you respond to the bell (e.g. please "Enter" in the console after the
system bell rings), it restarts the alarm and will ring again after your
specified time. Use control-c to exit the alarm completely.

sorno_amazon_reviews_scrape.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A script to scrape Amazon product reviews from the web page.

sorno_amazon_wishlist_scrape.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A script to scrape items from an Amazon wishlist. The script only works for
wishlists which are "Public". You can change the settings by following the
instruction in:
http://www.amazon.com/gp/help/customer/display.html?nodeId=501094

sorno_appcache_generator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate an appcache file to be used for html5 application cache of a web
application. The goal is to make the whole web app cached, so the app can be
run offline.

sorno_attach_realdate.py
~~~~~~~~~~~~~~~~~~~~~~~~
Attaches the actual time in human readable format for timestamps found in
coming lines.

Example::

    $ cat /tmp/abc
    once upon a time 1455225387 there is
    1455225387 something called blah
    and 1455225387
    then foo

    $ cat /tmp/abc |python scripts/sorno_attach_realdate.py
    once upon a time 1455225387(2016-02-11 13:16:27) there is
    1455225387(2016-02-11 13:16:27) something called blah
    and 1455225387(2016-02-11 13:16:27)
    then foo


sorno_cloud_vision.py
~~~~~~~~~~~~~~~~~~~~~
sorno_cloud_vision.py makes using the Google Cloud Vision API easier.

Doc: https://cloud.google.com/vision/docs

The script generates requests for the given photos, sends the requests to Cloud
Vision, then puts the results into the corresponding response files.

sorno_compress_photos.py
~~~~~~~~~~~~~~~~~~~~~~~~
Compresses all photos in a directory to jpg quality.

sorno_download_all.py
~~~~~~~~~~~~~~~~~~~~~
Downloads all items from all links from a URL.

sorno_dropbox.py
~~~~~~~~~~~~~~~~
Provides utilities to work with dropbox just like the official dropbox cli
(http://www.dropboxwiki.com/tips-and-tricks/using-the-official-dropbox-command-line-interface-cli),
but in a script instead of a REPL way. sorno_dropbox also has higher level
features like copying directories recursively.

sorno_email.py
~~~~~~~~~~~~~~
Sends a simple email with plain text

The script first tries to use your system Mail Transfer Agent(MTA) configured,
otherwise, it prompts for login to use Gmail SMTP server.

sorno_facts.py
~~~~~~~~~~~~~~~~~~~~
Prints out a random fact for fun

sorno_gdoc.py
~~~~~~~~~~~~~~~~~
A command line client for accessing Google Docs. The API doc used to implement
it is in https://developers.google.com/drive/web/quickstart/quickstart-python

You can search for a file and download its content (only if it's a doc).

sorno_gdrive.py
~~~~~~~~~~~~~~~~~~~
A command line client for Google Drive. The API doc used to implement this is
in
https://developers.google.com/drive/web/quickstart/quickstart-python

Currently, you can upload files with the script.

sorno_grepchunks.py
~~~~~~~~~~~~~~~~~~~
Oftenly, you want to treat multiple lines as one chunk and see if it matches a
regex. If it does, you want to print out the whole chunk instead of the only
line that matches the regex. sorno_grepchunks lets you define what a chunk
is by giving a chunk starting regex, that is, all the lines starting from the
line that matches the regex and before the next match are treated as one
chunk. You can then apply another regex to match against it.

sorno_gtasks.py
~~~~~~~~~~~~~~~
A script version of Google Tasks

sorno_ls.py
~~~~~~~~~~~
sorno_ls.py is just like the Unix "ls" command

sorno_pick.py
~~~~~~~~~~~~~
A script to prompt for choosing items generated from different sources, then
print those items out. For example, if you have a script to generate common
directories that you use, e.g. gen-fav-dir.sh, you can put the following in
your .bashrc, assuming sorno_pick.py and gen-fav-dir.sh are in your PATH::

    $ alias cdf='cd $(sorno_pick.py -c gen-fav-dir.sh)'

Then you can just type::

    $ cdf

And you will be given a list of directories to "cd" to.

P.S. You probably want to set the alias to the following::

    $ alias cdf='tmp="cd $(sorno_pick.py -c gen-fav-dir.sh)";history -s "$tmp";$tmp'

This ensures the history is inserted in a useful way, e.g. when you run
"history", you see the actual command instead of just "cdf".

sorno_podcast_downloader.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Downloads podcasts given a feed url.

The downloaded podcasts have useful file
names (e.g contain the title of the podcast and prefixed by the published
date).

sorno_realdate.py
~~~~~~~~~~~~~~~~~
Prints the human readable date for timestamps

Example::

    $ sorno_realdate.py 1455223642 1455223642000 1455223642000000 1455223642000000000
    1455223642: 2016-02-11 12:47:22-0800 PST in s
    1455223642000: 2016-02-11 12:47:22-0800 PST in ms
    1455223642000000: 2016-02-11 12:47:22-0800 PST in us
    1455223642000000000: 2016-02-11 12:47:22-0800 PST in ns

sorno_reduce_image_sizes.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Saves images with reduced sizes.

Reduces the sizes of all images in a directory and its subdirectories by
saving them with lower quality jpg format. The directory structure is
preserved but the new directory is created with a timestamp suffix.

sorno_rename.py
~~~~~~~~~~~~~~~
sorno_rename.py renames files given regex for matching names of the
existing files and using backreferences for filenames to be renamed to.

sorno_replace_thrift_const.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Replaces constants with literal values for a thrift file except for the
declaration. This is mainly for thrift compilers which cannot handle constants
within lists or other collection structures.

sorno_scrape_peg_list_1000.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scrapes the 1000 pegs from http://www.rememberg.com/Peg-list-1000/

sorno_spacefill.py
~~~~~~~~~~~~~~~~~~
Fills up the disk space with a specific size of garbage data.

sorno_stock_quote.py
~~~~~~~~~~~~~~~~~~~~
Gets stock quotes and other information for stock symbols.

The script can print real-time or close to real-time stock quotes, historical
quotes, and also fundamental ratios for the stock (company).

sorno_summarize_code.py
~~~~~~~~~~~~~~~~~~~~~~~
Prints a summary of the code file.

It makes the layout of the code to be read easily. Currently it only supports
python files.

sorno_top_size_files.py
~~~~~~~~~~~~~~~~~~~~~~~
Prints the top files in terms of sizes.

Prints the top files in terms of sizes under a directory or its subdirectories
size

Using scripts involving Google App API
---------------------------------------
For scripts like "sorno_gdoc.py", "sorno_gdrive.py" and "sorno_gtasks.py", a
**Google App project** is required to account for the quota of using the API.
You need to get an **OAuth2** **client id** and **secret** for your Google App
project, then export them as environment variables
"GOOGLE_APP_PROJECT_CLIENT_ID" and "GOOGLE_APP_PROJECT_CLIENT_SECRET"
respectively (replace "xxx" and "yyy" with your actual values) before running
the script::

    export GOOGLE_APP_PROJECT_CLIENT_ID='xxx'
    export GOOGLE_APP_PROJECT_CLIENT_SECRET='yyy'

You probably want to put the two lines above in your bashrc file.

You can get the oauth2 client id and secret by the following steps:

1) Choose a Google App project or create a new one in
   https://console.developers.google.com/project

2) After you have chosen a Google App Project, you then go to the tab "APIs &
   auth" on the left.

3) Click on the APIs subtab, and search for the API needed for the script you
   want to use. The help page of the script tells you what API your project
   needs. For example, sorno_gtasks.py needs the Tasks API with the scope
   'https://www.googleapis.com/auth/tasks'. Enable it.

4) Go to the "Credentials" subtab, click "Add credentials", choose "OAuth 2.0
   client ID", enter some information on the OAuth consent screen if prompted.
   In that screen, only email address and product name are required to be
   filled out. For the *Application type*, choose "Other".

5) After the credentials is created, click on it and you should see your
   **Client ID** and **Client secret** there.

Troubleshooting
~~~~~~~~~~~~~~~
If you are getting some import error when running the script, make sure you
have the newest Google API Client Library for Python. You can find the
installation instruction here:
https://developers.google.com/api-client-library/python/start/installation

Development
-----------
Start
~~~~~
A sample of a script can be obtained from *python/script_template.py* in
https://github.com/hermantai/samples.

Unit testing
~~~~~~~~~~~~
You can run the unit tests in the *scripts/tests* directory. First, set up the
testing environment by running::

    $ source setup_test_env.sh

If you have installed sorno-py-scripts in your machine, the *sorno* library
from the installation is used instead of your local changes because of
easy-install messing with the search path. In that case you need to either
remove the egg manually or bump up the version and install it with your local
changes to override the existing version.

Then you can run individual unit tests with::

    $ python scripts/tests/test_xxx.py

Deployment
~~~~~~~~~~
The only deployment destinations for now is github and PyPI. In github, this
project resides in the sorno-py-scripts project:
https://github.com/hermantai/sorno-py-scripts

To deploy to PyPI, first install twine::

    $ pip install twine

Then you can use the script to deploy to PyPI::

    $ ./pypi_deploy_with_twine.sh

Use **sudo** if you encounter permission issues when running the commands.

Use the following if you get an error saying "twine cannot be found" even
twine is on your PATH::

    sudo env "PATH=$PATH" ./pypi_deploy_with_twine.sh

If twine does not work, use the old school::

    $ ./pypi_deploy.sh
