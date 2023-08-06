*********************
collective.js.videojs
*********************

.. contents:: Table of Contents

Introduction
============

This addon provide jQuery File Upload as browser resource.

Version: 9.12.3

Resources::

  ++resource++collective.js.fileupload/
  ++resource++collective.js.fileupload/js/video.js
  ++resource++collective.js.fileupload/js/video.min.js
  ++resource++collective.js.fileupload/js/cors/jquery.postmessage-transport.js
  ++resource++collective.js.fileupload/js/cors/jquery.xdr-transport.js
  ++resource++collective.js.fileupload/js/vendor/jquery.ui.widget.js
  ++resource++collective.js.fileupload/js/app.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-angular.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-audio.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-image.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-jquery-ui.js
  ++resource++collective.js.fileupload/js/jquery.fileupload.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-process.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-ui.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-validate.js
  ++resource++collective.js.fileupload/js/jquery.fileupload-video.js
  ++resource++collective.js.fileupload/js/jquery.iframe-transport.js
  ++resource++collective.js.fileupload/js/main.js
  ++resource++collective.js.fileupload/css/demo.css
  ++resource++collective.js.fileupload/css/demo-ie8.css
  ++resource++collective.js.fileupload/css/jquery.fileupload.css
  ++resource++collective.js.fileupload/css/jquery.fileupload-noscript.css
  ++resource++collective.js.fileupload/css/jquery.fileupload-ui.css
  ++resource++collective.js.fileupload/css/jquery.fileupload-ui-noscript.css
  ++resource++collective.js.fileupload/img/loading.gif
  ++resource++collective.js.fileupload/img/progressbar.gif

About jQuery File Upload
========================

File Upload widget with multiple file selection, drag&drop support, progress bar, validation and preview images, audio and video for jQuery.
Supports cross-domain, chunked and resumable file uploads. Works with any server-side platform (Google App Engine, PHP, Python, Ruby on Rails, Java, etc.) that supports standard HTML form file uploads. https://blueimp.github.io/jQuery-File-Upload/

Don't Panic
===========

Installation
------------

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.js.fileupload`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        collective.js.fileupload

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

There is no need to apply a profile.
