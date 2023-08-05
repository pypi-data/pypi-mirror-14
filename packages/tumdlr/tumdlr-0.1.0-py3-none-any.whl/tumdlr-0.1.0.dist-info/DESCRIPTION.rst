tumdlr (Tumblr Downloader)
==========================

|Scrutinizer Code Quality|

Introduction
============

Tumdlr is a command line application for generating and maintaining
Tumblr blog archives.

It works almost entirely using Tumblr's own
`API <https://www.tumblr.com/docs/en/api/v2>`__ instead of relying on
web scraping methods, offering vastly superior performance without the
risk of breaking with future site updates.

This application is currently in pre-alpha status and currently only
supports archiving photo posts with limited configuration options
available.

Features
--------

Tumdlr currently supports archiving the following types of posts: \*
Photos (including linked photos) \* Videos (support for external video
embeds, such as YouTube, is provided via
`youtube-dl <https://rg3.github.io/youtube-dl/>`__) \* Audio \* Text /
regular posts (in both plain text and HTML)

In addition to, Tumdlr is able to track and update previously archiving
blogs without needing to re-download existing posts.

License
-------

::

    The MIT License (MIT)

    Copyright (c) 2015 Makoto Fujimoto

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/FujiMakoto/tumdlr/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/FujiMakoto/tumdlr/?branch=master


