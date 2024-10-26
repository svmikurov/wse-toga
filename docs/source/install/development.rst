==============
Developer mode
==============

.. seealso::

   **Official documentation:**

   `BeeWare Tutorial <https://docs.beeware.org/en/latest/index.html>`_

   `Toga <https://toga.readthedocs.io>`_

`Install dependencies <https://docs.beeware.org/en/latest/tutorial/tutorial-0.html#install-dependencies>`_

Install app
-----------

.. code-block:: console

   git clone git@github.com:svmikurov/wse-toga.git
   cd wse-toga/
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.dev.txt
   make ruff test

Run development mode
--------------------

.. code-block:: console

   make start
