from django.utils.html import format_html
from django.conf import settings

from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_css')
def allow_font_awesome_icons():
    return format_html(
        '<link rel="stylesheet" href="'
        + settings.STATIC_URL
        + 'wagtailblocks_cards/css/wagtailblocks_cards.css">'
    )
