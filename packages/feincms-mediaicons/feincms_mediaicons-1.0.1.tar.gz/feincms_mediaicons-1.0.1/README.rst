==================
feincms_mediaicons
==================

feincms_mediaicons adds default rendering functionality to some of the most
common mediafile types. By default, the icon corresponding to a certain 
filetype is displayed next to the mediafile link

Installation
------------

1. Add "feincms_mediaicons" to your INSTALLED_APPS; it is recommended
   to include it below your own apps so that you can later override templates 
   bundled with this plugin in your own code (since django matches templates in
   order defined by INSTALLED_APPS, if you put feincms_mediaicons above your 
   apps, it will ignore your overrides). Like this::

    INSTALLED_APPS = (
        # ...
        'your_app_one'
        'your_app_two'
        'feincms_mediaicons',
    )

2. If necessary, override templates in::

    project_dir/app/templates/content/mediafile/<file_extension>.html

3. If necessary, override static files (icons) in::

    project_dir/app/static/mediafile/<file_extension>.png

No migrations required (this module contains static files and templates only)
