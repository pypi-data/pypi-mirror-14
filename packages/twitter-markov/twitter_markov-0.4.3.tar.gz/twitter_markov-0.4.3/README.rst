twitter markov
==============

Create markov chain ("\_ebooks") accounts on Twitter

The audience for this library is those with at least basic Python
experience. Before you set this up, you'll need:

-  A twitter account
-  A twitter application (register at
   `dev.twitter.com <http://dev.twitter.com>`__) with authentication
   keys for the account (`read more <https://dev.twitter.com/oauth>`__)
-  A corpus for the bot to learn, which can be a text file or a Twitter
   archive. Several thousand lines are needed to get decent results,
   with fewer than 100 or so it won't work at all.

Install
-------

Run ``pip install twitter_markov``, or download/clone the package and
run ``python setup.py install``. Feel free to use a virtualenv, if
you're into that.

Corpus Pocus
------------

"Corpus" is just a fancy-schmancy word for "a bunch of text".
``twittermarkov`` expects a corpus that's a text file with one tweet per
line.

The ``twittermarkov corpus`` command will create such a file from a
Twitter archive, with options to ignore replies or retweets, and to
filter out mentions, urls, media, and/or hashtags.

When reading an archive, these arguments use the tweet's metadata to
precisely strip the offending content. This may not work well for tweets
posted before 2011 or so. For text files or older tweets, a regular
expression search is used.

.. code:: bash

    # Usage is twittermarkov corpus archive output
    # This creates the file corpus.txt
    twittermarkov corpus twitter/archive/path corpus.txt

    twittermarkov corpus --no-retweets --no-replies twitter/archive/path corpus-no-replies.txt
    # Teweets like this will be ignored:
    # RT @sample I ate a sandwich

    # Tweets like this will be read in without the @sample:
    # @sample Was it tasty?

All the filtering options: \* ``--no-retweets`` - skip retweets \*
``--no-replies`` - filter out replies (keeps the tweet, just removes the
starting username) \* ``--no-mentions`` - filter out mentions \*
``--no-urls`` - filter out urls \* ``--no-media`` - filter out media \*
``--no-hashtags`` - filter out hashtags

If you're using a Twitter archive, the archive argument should be the
tweet.csv file found in the archive folder (which usually has a long
name like 16853453\_3f21d17c73166ef3c77d7994c880dd93a8159c88).

Config
------

See the
`bots.yaml <https://github.com/fitnr/twitter_markov/blob/master/bots.yaml>`__
file for a full list of settings. Plug your settings in and save the
file as ``bots.yaml`` to your home directory or ``~/bots``. You can also
use JSON, if that's your thing.

At a minimum, your config file will need to look like this:

.. code:: yaml

    apps:
        example_app_name:
            consumer_key: ...
            consumer_secret: ...

    users:
        example_screen_name:

            key: ...
            secret: ...

            app: example_app_name

            # If you want your bot to continue to learn, include this
            parent: your_screen_name

Read up on `dev.twitter.com <https://dev.twitter.com/oauth/overview>`__
on obtaining authentication tokens.

First Tweet
-----------

Once a corpus is set up, the ``twittermarkov tweet`` command will send
tweets out. By default, the command will learn recent tweets from the
parent account and send one tweet.

The learning also won't happen if twittermarkov can't find it's previous
tweets, which might happen if there are problems with the Twitter API,
or your \_ebooks account has never tweeted.

Since learning depends on the ``_ebooks`` account having an existing
tweet, send a first tweet with the ``--no-learn`` flag.

.. code:: bash

    twittermarkov tweet --no-learn example_screen_name

To have your bot reply to mentions, use:

.. code:: bash

    twittermarkov tweet --reply example_screen_name

Automating
----------

On a \*nix system, set up a cron job like so:

::

    0 10-20 * * * twittermarkov tweet example_screen_name
    15,45 10-20 * * * twittermarkov tweet --reply example_screen_name

API
---

If you want to write a script to expand on twitter\_markov, you'll find
a fairly simple set of tools.

*class twitter\_markov.TwitterMarkov(screen\_name, corpus=None,
config=None, api=None)*

-  screen\_name - Twitter user account
-  corpus - Path to a corpus file, or a list of paths. If omitted,
   Twitter\_markov looks in its config for ``corpus`` and/or ``corpora``
   entries.
-  config - A dictionary of configuration settings. But default,
   twitter\_markov will try to read this from the bots.yaml file (see
   above)/
-  api - A tweepy-like API object. In the twitter\_markov class, this is
   a ``twitter_bot_utils.API`` object.
-  blacklist - A list of words to avoid generating

The first corpus in the found corpora (or in the config file) will be
the default. When using the class with more than corpus, you can specify
a corpus with the ``model`` keyword argument using the basename of the
given file, e.g. "special.txt" for the corpus stored at
"dir/special.txt".

Properties: \* recently\_tweeted - A list of the 20 (or
``config['checkback']``) most recent tweets from ``self.screen_name``.

Methods:

-  ``check_tweet(text)``: Check if a string contains blacklisted words
   or is similar to a recent tweet.
-  ``reply(status, model=None): Compose a reply to the given``\ tweepy.Status\`.
-  ``reply_all(model=None)``: Reply to all mentions since the last time
   ``self.screen_name`` sent a reply tweet.
-  ``compose(model=None, max_len=140)``: Returns a string generated from
   "model" (or the default model).
-  ``tweet(model=None)``: Post a tweet composed by "model" (or the
   default model).
-  ``learn_parent(corpus=None, model=None)``: Add recent tweets from the
   parent account (since the last time ``self.screen_name`` tweeted) to
   the corpus. This is subject to the filters described in
   ``bots.yaml``.

Example
~~~~~~~

This assumes a corpus file (``corpus.txt``) and config file
(``config.yaml``).

.. code:: python

    from twitter_markov import TwitterMarkov

    tm = TwitterMarkov('example_screen_name', 'corpus.txt', config_file='config.yaml')
    tweet = tm.compose()

    # do something more with tweet, or use the Tweepy API in a different way
    tm.api.update_status(tweet)

