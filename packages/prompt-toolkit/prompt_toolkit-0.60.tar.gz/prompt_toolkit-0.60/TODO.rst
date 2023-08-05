

- Focus stack needs to accept values other than `None`. This way we can better give the sidebar and exit message focus in ptpython, and it doesn't break focus in unpredictable ways in ptpdb.

- Margins in BufferControl needs to be rendered independently. That way we can clean up code in the Screen class (which should not be responsible for calling margins.) The Screen class should however keep a mapping of the line numbers to input lines. This will also make it possible to invalidate margins independently of the main content. (Probably it's not worth having invalidation on the margins -- it's not heavy to calculate.)

- Find a way to support backgrounds. A.k.a: find a way to eleminate Pygments.

- support editing of larger buffers.


Eleminate pygments
------------------

We need two things:
- Tokens to identify chunks of text.
- A stylesheet.
For both, we still want to be able to use Pygments, by wrapping them, without loosing any performance.


Pygments limitations:
- Tokens have just one class, unlike CSS. A <span> in HTML can have several classes, where each class contributes to a part of the styling. (E.g. the background.)

Token.History.Something


Editing of larger buffers
-------------------------

We need two things:
- A way to incrementally edit text of large buffers. (Keeping history.)
- A way to incrementally lex the result of such a large buffer.


Renames:
-------

WindowRenderInfo.rendered_height -> window_height
WindowRenderInfo.input_line_to_screen_line -> should become property.
