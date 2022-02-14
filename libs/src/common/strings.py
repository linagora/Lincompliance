#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def has_ext(name: str, ext_list: list) -> bool:
    """
    Check if a name has an extension from the ext list
    @param name:
    @param ext_list:
    @return: True if the name has extension from the ext_list, False otherwise
    """
    return '.' in name and \
           name.rsplit('.', 1)[1].lower() in ext_list
