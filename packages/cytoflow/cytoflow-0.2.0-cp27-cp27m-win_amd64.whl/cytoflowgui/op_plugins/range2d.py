#!/usr/bin/env python2.7

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on Apr 25, 2015

@author: brian
'''

from traits.api import provides, Callable
from traitsui.api import View, Item, EnumEditor, Controller
from envisage.api import Plugin, contributes_to
from pyface.api import ImageResource

from cytoflow.operations.range2d import Range2DOp, RangeSelection2D
from cytoflow.views.i_selectionview import ISelectionView

from cytoflowgui.op_plugins.i_op_plugin \
    import IOperationPlugin, OpHandlerMixin, PluginOpMixin, OP_PLUGIN_EXT, shared_op_traits
from cytoflowgui.view_plugins.i_view_plugin import ViewHandlerMixin, PluginViewMixin, shared_view_traits
from cytoflowgui.subset_editor import SubsetEditor

class Range2DHandler(Controller, OpHandlerMixin):
    
    def default_traits_view(self):
        return View(Item('object.name'),
                    Item('object.xchannel',
                         editor=EnumEditor(name='handler.previous_channels'),
                         label = "X Channel"),
                    Item('object.xlow', label = "X Low"),
                    Item('object.xhigh', label = "X High"),
                    Item('object.ychannel',
                         editor=EnumEditor(name='handler.previous_channels'),
                         label = "Y Channel"),
                    Item('object.ylow', label = "Y Low"),
                    Item('object.yhigh', label = "Y High"),
                    shared_op_traits) 
        
class RangeView2DHandler(Controller, ViewHandlerMixin):
    def default_traits_view(self):
        return View(Item('object.name', 
                         style = 'readonly'),
                    Item('object.xchannel', 
                         label = "X Channel", 
                         style = 'readonly'),
                    Item('object.xscale',
                         label = "X Scale"),
                    Item('object.ychannel',
                         label = "Y Channel",
                         style = 'readonly'),
                    Item('object.yscale',
                         label = "Y Scale"),
                    Item('object.huefacet',
                         editor=EnumEditor(name='handler.conditions'),
                         label="Color\nFacet"),
                    Item('_'),
                    Item('object.subset',
                         label = "Subset",
                         editor = SubsetEditor(experiment = 'handler.wi.previous.result')),
                    shared_view_traits)

@provides(ISelectionView)
class Range2DSelectionView(RangeSelection2D, PluginViewMixin):
    handler_factory = Callable(RangeView2DHandler)
    
class Range2DPluginOp(Range2DOp, PluginOpMixin):
    handler_factory = Callable(Range2DHandler)

@provides(IOperationPlugin)
class Range2DPlugin(Plugin):
    """
    class docs
    """
    
    id = 'edu.mit.synbio.cytoflowgui.op_plugins.range2d'
    operation_id = 'edu.mit.synbio.cytoflow.operations.range2d'

    short_name = "Range 2D"
    menu_group = "Gates"
    
    def get_operation(self):
        return Range2DPluginOp()
    
    def get_default_view(self):
        return Range2DSelectionView()

    def get_icon(self):
        return ImageResource('range2d')
    
    @contributes_to(OP_PLUGIN_EXT)
    def get_plugin(self):
        return self