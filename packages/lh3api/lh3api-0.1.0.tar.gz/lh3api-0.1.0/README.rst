Configuration
============

In ~/.lh3/config::

    [default]
    server = libraryh3lp.com
    timezone = UTC
    salt = "you should probably change this"

The `salt` is used when generating system-level utility accounts.
This is not something you do often.  If your `salt` is unique, your
passwords will be unique.

In ~/.lh3/credentials::

    [default]
    username = <ADMIN_USER>
    password = <ADMIN_PASS>

    [test]
    username = <TEST_USER>
    password = <TEST_PASS>

You can define different profiles (`test` above) that have different
levels of access to the system, or access to different parts of the
system.
