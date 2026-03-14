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

    daten = anvil.server.call("hole_fahrer_plot_daten")

    fig = go.Figure()

    for fahrername, werte in daten.items():
      fig.add_trace(go.Scatter(
        x=werte["rennen"],
        y=werte["punkte"],
        mode="lines+markers",
        name=fahrername
      ))

    fig.update_layout(
      title="Punkte der Fahrer pro Rennen",
      xaxis_title="Rennen",
      yaxis_title="Punkte",
      hovermode="x unified"
    )

    self.plot_1.figure = fig

  @handle("plot_1", "click")
  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass
