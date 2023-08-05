#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Simon Perkins
#
# This file is part of montblanc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from montblanc.slvr_config import (SolverConfiguration,
    SolverConfigurationOptions)
from montblanc.impl.biro.slvr_config import (BiroSolverConfiguration,
    BiroSolverConfigurationOptions)

__PADDING = ' '*4

def __fmt_description(descriptor, strings):
    import collections

    l = ['%s:' % descriptor]
    if isinstance(strings, str):
        l.append(__PADDING + strings)
    elif isinstance(strings, collections.Iterable):
        l.extend([__PADDING + str(s) for s in strings])

    return l

def __gen_opt_str_list(descriptions):
    """
    Generates a list of strings describing
    options, their defaults and the valid
    values that they may be set to.

    Parameters:
        descriptions: dict
            A dictionary defining the option.
            {
                'version' : {
                    'default' : 'v1',
                    'valid' : ['v1','v2','v3','v4'],
                    'description' : 'The application version'
                },
                'auto_correlations' : {
                    'default' : False,
                    'valid' : [True, False],
                    'description' : 'Consider auto-correlations'
                }
            }
    """
    l = []

    iterator = descriptions.iteritems()

    for option, info in iter(sorted(iterator)):
        l.append('Option:\n%s%s' % (__PADDING,option))

        default = info.get(SolverConfigurationOptions.DEFAULT)
        l.append('Default Value:\n%s%s' % (__PADDING,default))

        valid = info.get(SolverConfigurationOptions.VALID, None)
        if valid is not None:
            l.append('Valid Values:\n%s%s' % (__PADDING,valid))

        description = info.get(SolverConfigurationOptions.DESCRIPTION, None)
        if description is not None:
            l.extend(__fmt_description('Description', description))


        l.append('\n')

    return l

def describe_options():
    """
    Generates a string describing
    options, their defaults and the valid
    values that they may be set to
    """    
    opt_list = __gen_opt_str_list(SolverConfigurationOptions.descriptions)
    opt_list.extend(__gen_opt_str_list(BiroSolverConfigurationOptions.descriptions))

    return '\n'.join(opt_list)