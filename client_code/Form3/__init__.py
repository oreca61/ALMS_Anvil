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

    daten = anvil.server.call("hole_fahrer_endstand")
    print(daten)

    self.plot_1.data = [
      go.Bar(
        x=daten["punkte"],
        y=daten["fahrer"],
        orientation="h"
      )
    ]

    self.plot_1.layout = go.Layout(
      title="Endstand der Fahrer",
      xaxis=dict(title="Punkte"),
      yaxis=dict(title="Fahrer", autorange="reversed"),
      margin=dict(l=260, r=40, t=60, b=40)
    )


  @handle("plot_1", "click")
  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass
