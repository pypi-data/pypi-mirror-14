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

"""
Created on Feb 24, 2015

@author: brian
"""

from traits.api import provides, Callable
from traitsui.api import View, Item, Controller, EnumEditor
from envisage.api import Plugin, contributes_to
from pyface.api import ImageResource

from cytoflow import HistogramView

from cytoflowgui.subset_editor import SubsetEditor
from cytoflowgui.color_text_editor import ColorTextEditor
from cytoflowgui.view_plugins.i_view_plugin \
    import IViewPlugin, VIEW_PLUGIN_EXT, ViewHandlerMixin, PluginViewMixin, shared_view_traits
    
class HistogramHandler(Controller, ViewHandlerMixin):
    """
    docs
    """
    
    def default_traits_view(self):
        return View(Item('object.name'),
                    Item('object.channel',
                         editor=EnumEditor(name='handler.channels'),
                         label = "Channel"),
                    Item('object.scale'),
                    Item('object.xfacet',
                         editor=EnumEditor(name='handler.conditions'),
                         label = "Horizontal\nFacet"),
                    Item('object.yfacet',
                         editor=EnumEditor(name='handler.conditions'),
                         label = "Vertical\nFacet"),
                    Item('object.huefacet',
                         editor=EnumEditor(name='handler.conditions'),
                         label="Color\nFacet"),
                    Item('_'),
                    Item('object.subset',
                         label="Subset",
                         editor = SubsetEditor(experiment = "handler.wi.result")),
                    shared_view_traits)
    
class HistogramPluginView(HistogramView, PluginViewMixin):
    handler_factory = Callable(HistogramHandler)

@provides(IViewPlugin)
class HistogramPlugin(Plugin):
    """
    classdocs
    """

    id = 'edu.mit.synbio.cytoflowgui.view.histogram'
    view_id = 'edu.mit.synbio.cytoflow.view.histogram'
    short_name = "Histogram"
    
    def get_view(self):
        return HistogramPluginView()
    
    def get_icon(self):
        return ImageResource('histogram')

    @contributes_to(VIEW_PLUGIN_EXT)
    def get_plugin(self):
        return self