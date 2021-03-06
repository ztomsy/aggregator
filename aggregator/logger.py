#!/usr/bin/env python
# encoding: utf-8
import logging

class CustomLogger:
    def setup_custom_logger(name: str='', log_level=logging.INFO):
        formatter = logging.Formatter(fmt='%(asctime)s - '
                                            '%(name)s - '
                                            '%(funcName)s - '
                                            '%(levelname)s - '
                                            '%(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.addHandler(handler)
        return logger