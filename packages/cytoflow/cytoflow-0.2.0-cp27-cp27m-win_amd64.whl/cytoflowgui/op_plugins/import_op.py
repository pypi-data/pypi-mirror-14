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
Created on Mar 15, 2015

@author: brian
"""
# 
# if __name__ == '__main__':
#     from traits.etsconfig.api import ETSConfig
#     ETSConfig.toolkit = 'qt4'
# 
#     import os
#     os.environ['TRAITS_DEBUG'] = "1"

from traitsui.api import View, Item, Controller
from traits.api import Button, Property, cached_property, provides, Callable, \
                       Bool
from pyface.api import OK as PyfaceOK
from envisage.api import Plugin

from cytoflow import ImportOp
from cytoflow.operations.i_operation import IOperation
                       
from cytoflowgui.import_dialog import ExperimentDialog
from cytoflowgui.op_plugins.i_op_plugin \
    import IOperationPlugin, OpHandlerMixin, PluginOpMixin, shared_op_traits


class ImportHandler(Controller, OpHandlerMixin):
    """
    A WorkflowItem that handles importing data and making a new Experiment
    """
    
    import_event = Button(label="Edit samples...")
    samples = Property(depends_on = 'wi.result')
    events = Property(depends_on = 'wi.result')
    
    def default_traits_view(self):
        return View(Item('handler.import_event',
                         show_label=False),
                    Item('handler.samples',
                         label='Samples',
                         style='readonly',
                         visible_when='handler.wi.result is not None'),
                    Item('handler.events',
                         label='Events',
                         style='readonly',
                         visible_when='handler.wi.result is not None'),
                    Item('object.coarse',
                         label="Coarse\nimport?",
                         visible_when='handler.wi.result is not None'),
                    Item('object.coarse_events',
                         label="Events per\nsample",
                         visible_when='handler.wi.result is not None and object.coarse == True'),
                    shared_op_traits)
        
    def _import_event_fired(self):
        """
        Import data; save as self.result
        """

        d = ExperimentDialog()

        d.model.init_model(self.model)
            
        d.size = (550, 500)
        d.open()
        
        if d.return_code is not PyfaceOK:
            return
        
        d.model.update_import_op(self.model)
        
        d = None
        
    @cached_property
    def _get_samples(self):
        if self.wi.result is not None:
            return len(self.wi.operation.tubes)
        else:
            return 0
     
    @cached_property
    def _get_events(self):
        if self.wi.result is not None:
            return self.wi.result.data.shape[0]
        else:
            return 0

@provides(IOperation)
class ImportPluginOp(ImportOp, PluginOpMixin):
    handler_factory = Callable(ImportHandler)
    coarse = Bool(False)
            
@provides(IOperationPlugin)
class ImportPlugin(Plugin):
    """
    class docs
    """
    
    id = 'edu.mit.synbio.cytoflowgui.op_plugins.import'
    operation_id = 'edu.mit.synbio.cytoflow.operations.import'

    short_name = "Import data"
    menu_group = "TOP"
    
    def get_operation(self):
        return ImportPluginOp()
    
    def get_default_view(self):
        None