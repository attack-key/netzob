# -*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+
from gettext import gettext as _
import logging

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+


#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+


class Memory():
    """Memory:
            Definition of a memory, used to store variable values in a persisting and independent way.
    """

    def __init__(self):
        """Constructor of Memory:
        """
        # create logger with the given configuration
        self.log = logging.getLogger('netzob.Common.MMSTD.Dictionary.Memory.py')
        self.memory = dict()
        self.temporaryMemory = dict()

#+---------------------------------------------------------------------------+
#| Functions on memories                                                     |
#+---------------------------------------------------------------------------+
    def createMemory(self):
        """createMemory:
                Reinit the temporary memory and copy all values from the real memory in it.
        """
        self.temporaryMemory = dict()
        for key in self.memory.keys():
            self.temporaryMemory[key] = self.memory[key]

    def persistMemory(self):
        """persistMemory:
                Copy all values from the temporary memory into the real memory.
        """
        self.memory = dict()
        for key in self.temporaryMemory.keys():
            self.memory[key] = self.temporaryMemory[key]

    def cleanMemory(self):
        """cleanMemory:
                Remove all variables and values from real and temporary memories.
        """
        # self.memory = dict()  # TODO: impement this change in all calling functions.
        self.temporaryMemory = dict()

    def recallMemory(self):
        """recallMemory:
                Return all values store in the temporary memory.

                @return: the value of all variables in the temporary memory.
        """
        return self.temporaryMemory

    def printMemory(self):
        """printMemory:
                Debug functions which print all values in temporary memory.
        """
        self.log.debug("Memory map:")
        for id in self.temporaryMemory.keys():
            self.log.debug("> " + str(id) + " = " + str(self.temporaryMemory.get(id)))

#+---------------------------------------------------------------------------+
#| Functions on temporary memory elements                                    |
#+---------------------------------------------------------------------------+
    def hasMemorized(self, variable):
        """hasMemorized:
                Check if a variable is in the temporary memory.

                @param variable: the given variable we search in memory.
                @return: True if the variable has been found in the memory.
        """
        return variable.getId() in self.temporaryMemory.keys()

    def restore(self, variable):
        """restore:
                Copy back the value of a variable from the real memory in the temporary memory.

                @param variable: the given variable, the value of which we want to restore.
        """
        if variable.getId() in self.memory.keys():
            self.temporaryMemory[variable.getId()] = self.memory[variable.getId()]

    def memorize(self, variable):
        """memorize:
                Save the current value of a variable in memory.

                @param variable: the given variable, the value of which we want to save.
        """
        if variable.getCurrentValue() is not None:
            self.temporaryMemory[variable.getId()] = variable.getCurrentValue()

    def forget(self, variable):
        """forget:
                Remove a variable and its value from the temporary memory.
        """
        if self.hasMemorized(variable):
            self.temporaryMemory.popitem(variable.getId())

    def recall(self, variable):
        """recall:
                Return the value of one variable store in the temporary memory.

                @param variable: the variable, the value of which we are searching.
                @return: the value of the given variable in the temporary memory.
        """
        if self.hasMemorized(variable):
            return self.temporaryMemory[variable.getId()]
        else:
            return None
