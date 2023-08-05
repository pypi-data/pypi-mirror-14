#!/usr/bin/env python
# encoding: utf-8
import arrow


def get_time(string):
    local = arrow.get(string)
    return local.timestamp
