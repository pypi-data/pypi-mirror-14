===========
txttobitmap
===========

Simple script that converts given file to a bitmap.

The project emerged as a result of wondering "How to compress long text into a form that does not look scary for a human being?". While the generated images are obviously useless, it's still fun to play around with them.

Requirements
------------

* Python 3.2+

Installation
------------
::

    pip install txttobitmap


Usage
-----
::

    txttobitmap --mode {palette,grayscale} input output



* *mode* - one of the values:
  
  * *palette* - use 16 color palette (see: `Windows 16-color palette on Wikipedia <https://en.wikipedia.org/wiki/List_of_software_palettes#Microsoft_Windows_default_16-color_palette>`_) and represent each byte as two pixels
  * *grayscale* - represent each byte as grayscale pixel

* *input* - input file to convert
* *output* - output file to save the bitmap as
