#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
#
# Licensed under GPLv3, see file LICENSE in this source tree.

def cfm2ls(cfm = 0):
    return cfm * 0.4719475
    
def ls2cfm(ls = 0):
    return ls / 0.4719475