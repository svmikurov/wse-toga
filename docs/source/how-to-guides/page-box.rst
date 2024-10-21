========
Page box
========

Create the page box
===================

To create the :term:`page box` inherit it from :py:class:`~wse.base.BaseBox`.

**Box naming:** use constant to :term:`page box` naming.

Add widgets in class constructor of :term:`page box` to **comment chapters**:
  * Styles -- common widget styles (optionally);
  * Box widgets -- box widgets;
  * Widgets DOM -- box widget DOM.

Button move to page box
-----------------------

**Button naming:** ``btn_goto_boxname``.

Use as callback function for button ``on_press`` parameter the
`lambda <https://docs.python.org/3/reference/expressions.html#lambda>`_ with
:py:meth:`self.goto_box_handler(_, boxname) <wse.base.GoToBoxMixin.goto_box_handler>`
expression.

`on_press <https://toga.readthedocs.io/en/latest/reference/api/widgets/button.html#toga.Button.on_press>`_
-- is the handler to invoke when the button is pressed.

.. code-block:: python
   :caption: Example:

   ...
   def __init__():
       super().__init__()
       # Styles.
       btn_style = Pack(...)
       # Box widgets.
       btn_goto_boxname = (
           'Button name',
           on_press=lambda _: self.goto_box_handler(_, BOXNAME_BOX),
           style=btn_style,
       )
       ...
       # Widgets DOM.
       self.add(
           ...,
           btn_goto_boxname,
           ...,
       )
   ...

Add page box to app
===================

To add the box to app add the box class instance to :py:data:`wse.app.BOXES`,
and set name to it.

Use ``constance`` to naming.

Use box name to move to box.
