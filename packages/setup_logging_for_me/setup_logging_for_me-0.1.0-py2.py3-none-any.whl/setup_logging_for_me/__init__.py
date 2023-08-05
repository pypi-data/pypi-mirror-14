# -*- coding: utf-8 -*-

__author__ = 'Javier Andrés Mansilla'
__email__ = 'javimansilla@gmail.com'
__version__ = '0.1.0'

import logging


def basicConfig(**kwargs):
    options = {'level': logging.INFO,
            'format': "%(name)s %(levelname)s %(asctime)s - %(message)s"
    }
    options.update(kwargs)
    logging.basicConfig(**options)

