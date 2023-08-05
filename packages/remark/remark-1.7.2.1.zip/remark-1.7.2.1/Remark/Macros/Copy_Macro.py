# -*- coding: utf-8 -*-

# Description: Copy macro
# Detail: Copies the input to output.

# Remark 1.7.2
# Copyright (c) 2009 - 2016
# Kalle Rutanen
# Distributed under the MIT license (see license.txt).

from Remark.Macro_Registry import registerMacro

class Copy_Macro(object):
    def name(self):
        return 'Copy'

    def expand(self, parameter, remark):
        text = parameter
        return text

    def expandOutput(self):
        return True

    def htmlHead(self, remark):
        return []                

    def postConversion(self, remark):
        None

registerMacro('Copy', Copy_Macro())
