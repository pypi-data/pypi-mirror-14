# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
# This code is distributed under the two-clause BSD License.

import os
import os.path

from sentry.runner import main as sentry_main


def main():
    here = os.path.dirname(__file__)
    os.environ['SENTRY_CONF'] = os.path.join(here, 'sentry_conf.py')
    sentry_main()

if __name__ == '__main__':
    main()
