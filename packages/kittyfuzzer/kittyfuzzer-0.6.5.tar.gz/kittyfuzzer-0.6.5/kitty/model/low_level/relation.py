# Copyright (C) 2016 Cisco Systems, Inc. and/or its affiliates. All rights reserved.
#
# This file is part of Kitty.
#
# Kitty is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Kitty is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kitty.  If not, see <http://www.gnu.org/licenses/>.
'''
Relations between different fields.
'''
from kitty.core import KittyObject


class Relation(KittyObject):
    '''
    Describe a relation between two (or more) fields.

    .. example::

        let's assume we have two fields - A and S, and S holds the size of A.
        then, there is a Size Relation between A and S,
        where S is dependant on A,
    '''

    def __init__(self, dependency, func):
        '''
        :param dependency: the field the relation depends on
        :param func: function to apply on the return value of resolve
        '''
        super(Relation, self).__init__()
        self.dependency = dependency

    def resolve(self):
        dependency = self.resolve_dependency_field()
        result = self.resolution(dependency)
        if self.func:
            result = self.func(result)
        return result

    def resolution(self, dependency):
        '''
        different relation may result in different values,
        '''
        raise NotImplementedError('should be implemented in subclass %s' % (type(self).__name__))


class Size(Relation):

    def resolution(self, dependency):
        '''
        :return: the size of the dependency
        '''
        return len(dependency.render())


class IndexOf(Relation):

    def resolution(self, dependency):
        '''
        :return: the index of the field in its container (only count rendered fields)
        '''
        fields = dependency._enclosing.get_rendered_fields()
        if dependency in fields:
            return fields.index(dependency)
        return 0


class ElementCount(Relation):

    def resolution(self, dependency):
        '''
        :return: the count of direct fields in the dependency
        '''
        fields = dependency.get_rendered_fields()
        return len(fields)
