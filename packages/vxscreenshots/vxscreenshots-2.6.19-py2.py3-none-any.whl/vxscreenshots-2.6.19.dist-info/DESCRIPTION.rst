All rights reserved.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Description: About
        =====
        
        .. image:: https://img.shields.io/pypi/v/vxscreenshots.svg
            :target: https://pypi.python.org/pypi/vxscreenshots
        
        .. image:: https://travis-ci.org/Vauxoo/vxscreenshots.svg?branch=master
            :target: https://travis-ci.org/Vauxoo/vxscreenshots
        
        What is VXScreenshots?.
        -----------------------
        
        Basic Screenshots manager pushing and sharing automatically to Amazon S3 images
        and giving the link automatically to use them alá Skitch autoconfiguring your 
        Linux desktop environment with shutter properlly.
        
        This is a combination of tools Not a tool itself to have your Linux taking fast
        Screenshots.
        
        Why?.
        -----
        
        When you look for an alternative to `Skitch <https://evernote.com/skitch/>`_, an
        `evernote <https://evernote.com/>`_ extension which is
        pretty cool everybody mentioned `Shutter <http://shutter-project.org/>`_ 
        as the `best screenshot tool <http://askubuntu.com/questions/6558/what-screenshot-tools-are-available>`_
        on Linux (which is true) but it needs a lot of investigation and configurations to
        automate an important feature **Take the screenshot, edit it and sync it
        inmediatly with access with a direct link to embed it properlly**, even if this tool
        has some **upload features** they are full of marketing and noisy, with this
        little set of helpers in python, you can have your own server of images in
        Amazon s3 and preconfigure everything to work our of the box.
        
        See a little demonstration of what you can do.
        ----------------------------------------------
        
        .. image:: http://www.trend247.net/ico/play_video.png
            :target: https://youtube.com/vauxoomedia
            :align: center
        
        Features
        --------
        
        * Monitorize a folder and verify if you put an image there (png, jpeg, jpg, gif)
          the it is pushed automatically to your account on amazon S3.
        * Automatically create an index of **shared** files which you can get directly 
          into the clipboard.
        * Button to manage this behavior graphically avoiding go to the folder and make
          magic to get a shareable link.
        
          - Direct Link.
          - RST Code.
          - Html Code.
          - Markdown Code.
        
        * Helper script to run your favorite screenshots manager app.
        
        Where find more information?
        ----------------------------
        
        * `Documentation <http://vauxoo.github.io/vxscreenshots>`_.
        * `Installation <http://vauxoo.github.io/vxscreenshots/installation.html>`_.
        * `Source code <http://github.com/vauxoo/vxscreenshots>`_.
        * Commercial support and services at `Vauxoo <https://www.vauxoo.com>`_.
        
        
        
        ChangeLog
        =========
        
        - TODO: automate using gitchangelog
        
Keywords: vxscreenshots
Platform: Linux
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: End Users/Desktop
Classifier: Intended Audience :: System Administrators
Classifier: Intended Audience :: Customer Service
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Natural Language :: Spanish
Classifier: Programming Language :: Python :: 2.7
