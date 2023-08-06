The ledgrid module contains a single LEDGrid class which aims to be as
identical as possible to the public interface of the Raspberry Pi
`Sense HAT library`_, such that it is useful in mocking up software for
it and other such devices.

    .. image:: https://raw.githubusercontent.com/zeth/ledgrid/master/ledgrid-screenshot.png

Many existing Sense HAT LED demos and software will work using the
following import statement::

    from ledgrid import LEDGrid as SenseHat

However, the internal implementation is rather simplified and uses
pygame instead of the hardware HAT.

It requires pygame_ to be installed (not currently available through
pypi), an additional optional dependency is PIL (i.e. Pillow) which is
required by some features (notably scrolling text with the
show_message method).

It supports every Python version since 2.7.  It is contained in only
one Python file, so it can be easily copied into your project if you
don't want to use pypi. (The copyright and license notice must be
retained.)

At the bottom of the ledgrid.py file are some examples of usage.

Many thanks to Richard Hayler. The LED class, graphics, etc are based
on his `8x8GridDraw`_.

.. _`8x8GridDraw`: https://github.com/topshed/RPi_8x8GridDraw
.. _pygame: http://www.pygame.org
.. _`Sense HAT library`: https://pythonhosted.org/sense-hat/
