from ._anvil_designer import Form3Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form3(Form3Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    fig = go.Figure()

    fig.add_trace(go.Bar(
      x=[10, 20, 30],
      y=["A", "B", "C"],
      orientation="h"
    ))

    self.plot_1.figure = fig

  @handle("plot_1", "click")
  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass
