from wagtail.wagtailcore import hooks
from django.conf import settings
from django.utils.html import format_html_join


@hooks.register('insert_editor_js')
def editor_js():
    """
    Add extra JS files to the admin
    """
    js_files = [
        'wagtailgmaps/js/map-field.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script type="text/javascript" src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes


@hooks.register('insert_global_admin_css')
def admin_css():
    """
    Add extra CSS files to the admin
    """
    css_files = [
        'wagtailadmin/css/admin.css',
    ]

    css_includes = format_html_join(
        '\n', '<link rel="stylesheet" href="{0}{1}">', ((settings.STATIC_URL, filename) for filename in css_files))
    return css_includes
