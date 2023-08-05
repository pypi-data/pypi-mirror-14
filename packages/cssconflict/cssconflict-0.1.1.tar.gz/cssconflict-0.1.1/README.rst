cssconflict
========================================

.. code-block:: bash

  $ cat demo/white.css
  x {
      color: white;
  }
  $ cat demo/black.css
  x {
      color: black;
      display: inline-block;
  }
  $ cssconflict demo/white.css demo/black.css
  x {
    color: white; /* demo/white.css */
    color: black; /* demo/black.css */
  }

