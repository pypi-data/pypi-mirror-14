Changelog
=========

1.0.4
-----
    - Added ``complete_`` prefix to export directory.

1.0.3
-----
    - Temporarily disabled features and tests allowed again.

1.0.2
-----
    - Bugfixes based on feedback.
    - Temporary disabled some of tests and functionality (UUID in info name, checksums), because LTP subsystem is broken on their side.

1.0.1
-----
    - Bugfix of MANIFEST.in.

1.0.0
-----
    - URN:NBN incorporated into info file.
    - Some refactorings.
    - This version should successfully export package into to output directory and also trace the state changes.

0.11.0 - 0.11.3
----------------
    - Rewritten info_composer.
    - Rests fixed and significantly improved.
    - Added tracking feature to AMQP connector.
    - Fixed bug in packaging system.
    - Fixed bug in import system.
    - Attempt to fix the directory copying problem.

0.10.0
------
    - Fixed a lot of bugs.
    - Applied feedback from the LTP team.
    - Code for the MODS transformation moved into own module https://github.com/edeposit/marcxml2mods

0.9.0 - 0.9.2
-------------
    - Alpha version released for my colleague, which needs to use xslt_transformer.py.
    - Alpha 2. Fixed few bugs, added documentation.
    - Fixed some bugs, comments. Added more postprocessing.
    - Fixed bugs by the comments from mr. Bouchner.
    - Added content of the README.
    - ``reactToAMQPMessage()`` parameters modified.

0.1.0
-----
    - Project created.