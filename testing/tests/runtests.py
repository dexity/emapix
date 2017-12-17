#!/usr/bin/env python

# See Capture plugin
# http://somethingaboutorange.com/mrl/projects/nose/1.0.0/plugins/capture.html

import os
f = os.popen('nosetests -s --verbosity=2')
print f.read()
