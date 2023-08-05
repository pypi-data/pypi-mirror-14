
the standard library ``pwd``, ``grp`` and ``spwd`` are hard wired
to use ``/etc/passwd``, ``/etc/group`` and ``/etc/shadow`` respectively.

That makes them useless for managing these files when they reside somewhere else,
which is e.g. the case when using libnss.

This library reimplemenets the functionality by creating three classes that default
to opening the files under `/etc`, but which can be given explicit paths.

The original module level routines are now methods on the instances that return named tuples
with the fieldnames being the same as those from the stdlib modules.