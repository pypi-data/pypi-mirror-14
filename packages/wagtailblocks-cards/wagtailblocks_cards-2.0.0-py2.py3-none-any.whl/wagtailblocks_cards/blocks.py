from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.wagtailcore.blocks import ListBlock


class CardsBlock(ListBlock):
    @property
    def media(self):
        parent_media = super(CardsBlock, self).media
        cards_css = {
            'screen': (static('wagtailblocks_cards/css/wagtailblocks_cards.css'),)
        }
        cards_media = forms.Media(css=cards_css)
        return parent_media + cards_media

    def render_form(self, value, prefix='', errors=None):
        if errors:
            if len(errors) > 1:
                raise TypeError('CardsBlock.render_form unexpectedly received multiple errors')
            error_list = errors.as_data()[0].params
        else:
            error_list = None

        list_members_html = [
            self.render_list_member(child_val, "%s-%d" % (prefix, i), i,
                                    errors=error_list[i] if error_list else None)
            for (i, child_val) in enumerate(value)
        ]

        return render_to_string('wagtailblocks_cards/block_forms/cards.html', {
            'help_text': getattr(self.meta, 'help_text', None),
            'prefix': prefix,
            'list_members_html': list_members_html,
        })

    class Meta:
        if 'wagtailfontawesome' in settings.INSTALLED_APPS:
            icon = 'fa-clone'
