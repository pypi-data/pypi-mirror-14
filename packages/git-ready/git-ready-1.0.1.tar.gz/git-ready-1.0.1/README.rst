=============
``git ready``
=============

Get ready to commit, socially.

Traditional, branch-based git workflows are effectively anti-social when
combined with social code review tools, like `Gerrit
<https://www.gerritcodereview.com/>`_, where the philosophy of an effective
contributor is to share code early and often, long before it's in a "mergeable"
state.

Branch-based workflows presume that you are a lonely contributor, working on an
island, and that someday your commits will be mature enough to set sail for
civilization. Perhaps your commits are flawed, but that's okay, because they're
still private. You'll have time to clean them up later. No one has to see your
dirty shortcuts or your "obvious" mistakes.

Local branches ultimately foster offline iteration, void of human interaction,
where you can dwell on syntactic sugar, admiring the beauty of your art.
Confidently bolstered by whole days (or even weeks) spent in isolation, you
finally venture into the land of open source, only to have your masterpiece
shot down: "PEP8 violation. Did you even submit a TPS report?"

Instead, don't create local branches at all. Do a bit of work and kick it off
to Gerrit. Maybe it's still a work in progress, maybe it's not. The important
part is that code review is an important feedback loop, and **you should do
everything in your power to tighten your feedback loops.** Developers
communicate to each other in code. Share your commits as early as possible. Get
that inevitable feedback sooner.

Communicate more; iterate faster.

``git ready`` fosters a social workflow, where you have no chance of
accidentally committing directly to ``master``, and your best means of tracking
your work is to share it in Gerrit.

Installation
------------

.. image:: https://img.shields.io/pypi/v/git-ready.svg
   :target: https://pypi.python.org/pypi/git-ready

From `PyPi <https://pypi.python.org/pypi/git-ready>`_::

    $ pip install git-ready

Usage
-----

Start with your favorite git repository managed by Gerrit::

    $ git clone git@github.com:openstack/nova.git
    $ cd nova/

And instead of creating a branch, or accidentally committing to master, start
with ``git ready``::

    $ git ready

That's it! You're ready to commit on top of the master branch::

    $ git commit

So now what? You've effectively committed on an untracked branch. Sounds scary,
right? But remember, we have Gerrit! Send your changes off to Gerrit to turn
your unnamed branch into a social branch hosted by Gerrit::

    $ git review

Your code is up for review. And now you want to work on something else? Use
``git ready`` to get back onto the latest ``master`` branch and repeat the process::

    $ git ready
    $ git commit
    $ git review

Really, that's all there is to it.

Unless you want to work on upstream branches. Let's say you want to propose a
commit to the upstream ``stable/release`` branch::

    $ git ready stable/release
    $ git commit
    $ git review

``git ready`` will even track the remote branch for you without any fuss (yes,
``git ready`` just took away your one excuse to ever work directly with local
branches).
