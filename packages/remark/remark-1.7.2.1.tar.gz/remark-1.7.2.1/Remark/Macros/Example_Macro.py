# -*- coding: utf-8 -*-

# Description: Example macro

# Remark 1.7.2
# Copyright (c) 2009 - 2016
# Kalle Rutanen
# Distributed under the MIT license (see license.txt).

from Remark.Macro_Registry import registerMacro
from Remark.FileSystem import markdownRegion

class Example_Macro(object):
    def name(self):
        return 'Example'

    def expand(self, parameter, remark):
        scope = remark.scopeStack.top()

        className = scope.getString('Example.class_name', 'Example')

        text = remark.macro('Verbatim', parameter)
        text.append('')

        text += markdownRegion(
            remark.convert(parameter), 
            {'class' : className})

        return text

    def expandOutput(self):
        return False

    def htmlHead(self, remark):
        return []                

    def postConversion(self, remark):
        None

registerMacro('Example', Example_Macro())
