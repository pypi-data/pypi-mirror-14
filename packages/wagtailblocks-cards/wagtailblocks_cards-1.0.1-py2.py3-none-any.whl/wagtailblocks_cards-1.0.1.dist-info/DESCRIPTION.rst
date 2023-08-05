Wagtail Blocks: Cards
=====================

This Wagtail block can be used to add a series of cards. It is styled on the editor screen.

![Screenshot](screenshot.png)

Installation
------------

Run:

    pip install wagtailblocks-cards

Then add `wagtailblocks_cards` to your installed apps.

Usage
-----

Include the block wherever relevant and add it to any StreamField.

    from wagtailblocks_cards.blocks import CardsBlock

Then:

    body = StreamField([
      ('cards', CardsBlock())
    ])

Finally, template the block as usual.

Fields
------

Use the following names when templating:

* image - ImageChooserBlock
* title - CharBlock
* text - TextBlock
* link - PageChooserBlock


