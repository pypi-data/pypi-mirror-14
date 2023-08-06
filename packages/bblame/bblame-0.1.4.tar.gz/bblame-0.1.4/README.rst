bblame
======
``bblame`` is an interactive ncurses git blame viewer. Allowing you to explore the git history of a file. 

Features
--------
- Browse forwards and backwards through file history a commit at a time 
- Select a line and drill into the history past the commit that changed that line most recently
- Display the git ``show`` for the commit of any selected line
- Browse file history across file renames
- Search and colour support

Usage
-----
``bblame`` is a curses application. Usage will be displayed when called with no arguments or ``-h`` ``--help``::

    $ bblame 
    usage: bblame [-h] [--revision {revision}] [--debug]
                  filename [+{line_num} or +/{search_pattern}]
    bblame: error: too few arguments

To show available commands while running ``bblame`` use the ``h`` key, which will display the key to action mappings as below::

    KEYS: ACTION - DESCRIPTION
    --------------------------
    q:   Quit
       Quit the application

    /:   Search
       Search for single line strings

    n:   Next Search Match
       Jump to the next search match (in the downward direction)

    N:   Prev Search Match
       Jump to the prev search match (in the upward direction)

    v, s:   Visual Select Mode
       Enter visual select mode (only from normal mode)

    o:   Show/View Commit
       Show a commit selected by the visual mode cursor

    O:   Show/View file Commit
       Show the current file commit

    ENTER, d:   Drill Down
       Drill down past the commit highlighted in visual mode. Opens a new git blame

    <, ,:   Parent blame
       Open a new git blame to the parent of the current commit

    >, .:   Ancestor blame
       Open a new git blame to the ancestor of the current commit

    BACKSPACE, DC, f:   Pop Back
       Pop back to previous git object

    h:   Help
       Generate Help Message

 

Installation
------------
::

     sudo -H pip install bblame

or ::

    python setup.py install

Issue
-----
Issue tracker can be found here_

.. _here: https://bitbucket.org/niko333/betterblame/issues?status=new&status=open
