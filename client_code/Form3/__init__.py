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

    
    daten_endstand = anvil.server.call("hole_fahrer_endstand")
    

    self.plot_endstand.data = [

      
      go.Bar(
        
        x=daten_endstand["punkte"],
        y=daten_endstand["fahrer"],
        orientation="h"
        
      )
      
    ]

    self.plot_endstand.layout = go.Layout(
      
      title="Endstand der Fahrer" ,
      
      xaxis= dict(title="Punkte"),
      yaxis= dict(title="Fahrer" , autorange="reversed" ),
      
      margin = dict(l=260 , r=40 , t=60  , b=40)
    )

    # Verlauf
    daten_verlauf = anvil.server.call("hole_fahrer_verlauf")

    
    plot_daten = []

    for fahrername, werte in daten_verlauf.items():
      plot_daten.append(
        go.Scatter(
          
          x=werte["rennen"],
          y=werte["punkte"] ,
          
          mode="lines+markers",
          
          name=fahrername
        )
        
      )

    self.plot_verlauf.data = plot_daten

    self.plot_verlauf.layout = go.Layout(
      
      title= "Punkteverlauf der Fahrer" ,
      
      xaxis =dict(title="Rennen"),
      
      yaxis= dict(title="Kumulative Punkte"),
      margin= dict(l=80 , r=40 , t=60 , b=60)
    )


  @handle("plot_endstand", "click")
  def plot_endstand_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Form2")
