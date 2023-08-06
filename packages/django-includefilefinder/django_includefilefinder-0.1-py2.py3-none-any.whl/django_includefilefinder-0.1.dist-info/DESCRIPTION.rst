### Include file finder

This is static file finder for Django which will allow you to specify certain files instead of whole directories like FileSystemFinder do.


### 1. Setup
To install it just copy this folder into your project as an app and include it in your INSTALLED_APPS

include it in STATICFILES_FINDERS


    STATICFILES_FINDERS = [
        ...
        'includefilefinder.finder.IncludeFileFinder',
        ...
    ]



and add this extra STATICFILES list into your settings.py which will include all files which should be included using collectstatic


    STATICFILES = [
        # Bootstrap
        ('css', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/bootstrap/dist/css/bootstrap.min.css'))),
        ('css', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/bootstrap/dist/css/bootstrap-theme.min.css'))),
        ('js', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/bootstrap/dist/js/bootstrap.min.js'))),

        # Font Awesome
        ('css', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/css/font-awesome.min.css'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/fontawesome-webfont.eot'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/fontawesome-webfont.svg'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/fontawesome-webfont.ttf'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/fontawesome-webfont.woff'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/fontawesome-webfont.woff2'))),
        ('fonts', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/font-awesome/fonts/FontAwesome.otf'))),

        # JQuery
        ('js', os.path.abspath(os.path.join(BASE_DIR, 'bower_components/jquery/dist/jquery.min.js'))),
    ]


Remember to use this pattern

    STATICFILES = [
        ...
        ('folder', 'path/to/the/required.file'),
        ...
    ]


in order to achieve following file structure


    /django_app/app/local/folder/required.file


### License
------------
The MIT License (MIT)

