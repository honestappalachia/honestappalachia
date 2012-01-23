README
------

Website for Honest Appalachia.

Want to contribute?

First, [follow the documentation here to fork the repo](http://help.github.com/fork-a-repo/).

Now, you should create a virtualenv. First, [install virtualenv if you don't have it](http://pypi.python.org/pypi/virtualenv). `cd` into the forked repo (the first honestappalachia directory, which has this README in it). On the command line:

    $ virtualenv --no-site-packages --distribute env
    $ . env/bin/activate
    $ pip install -r requirements.txt
    $ deactivate # (when you're done)
