#!/usr/bin/env python

from emapix.i18n.countries import COUNTRIES

def generate_choices():
    s   = "\n\nCOUNTRY_CHOICES = (\n"
    choices = []
    for k, v in COUNTRIES.items():
        choices.append((v["alpha2"], v["name"]))
    s_choices   = sorted(choices, key=lambda x: x[1])
    for i in s_choices:
        s   += '    ("%s", "%s"),\n' % (i[0], i[1])
    s   += ")\n"
    print s


if __name__ == "__main__":
    generate_choices()

