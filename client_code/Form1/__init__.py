from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    return_value = anvil.server.call('query_database', 'SELECT name FROM gefaengnis')
    return_value = [entry[0] for entry in return_value]
    print(return_value)
    self.drop_down_ALMS_auswahl.items = return_value
    self.drop_down_ALMS_auswahl_change()

  @handle("drop_down_ALMS_auswahl", "change")
  def drop_down_ALMS_auswahl_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

    
