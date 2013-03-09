# -*- coding: utf-8 -*-

import cPickle as pickle

__all__ = (
    'process_color',
)


def hex_to_RGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return r, g, b


def round_color(color):
    """round color to some predifined color, (r, g, b) -> (r, g, b)"""
    r = color[0]
    g = (36 * (color[1] // 36)) + 3
    b = (85 * (color[2] // 85))
    return r, g, b


def color_to_db(color):
    return pickle.dumps(color)


def process_color(color):
    """ #RRGGBB -> rgba(%d, %d, %d, %d) """
    return color_to_db(round_color(hex_to_RGB(color)))


if __name__ == '__main__':
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings")
    from tasks.models import Entry
    colors = Entry.objects.all().values_list('color', flat=True).distinct()

    for c in colors:
        c_rgb = hex_to_RGB(c)
        c_rgb_nice = round_color(c_rgb)
        print "%s -> %s" % (c_rgb, c_rgb_nice)
