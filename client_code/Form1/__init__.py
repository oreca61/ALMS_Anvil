from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    rows = anvil.server.call('query_database',
                             "SELECT team_name FROM team ORDER BY team_name")

    # rows ist meist [(name,), (name,), ...]
    team_names = [r[0] if not isinstance(r, dict) else r["team_name"] for r in rows]

    self.drop_down_ALMS_auswahl.items = team_names

    # WICHTIG: zuerst etwas auswählen, sonst selected_value = None
    if team_names:
      self.drop_down_ALMS_auswahl.selected_value = team_names[0]
      self.drop_down_ALMS_auswahl_change()

  @handle("drop_down_ALMS_auswahl", "change")
  def drop_down_ALMS_auswahl_change(self, **event_args):
    team_name = self.drop_down_ALMS_auswahl.selected_value
    if not team_name:
      return

    # Quotes escapen, sonst knallt es bei Namen mit '
    team_name_sql = str(team_name).replace("'", "''")

    sql = f"""
SELECT DISTINCT
  t.team_id AS teamID,
  f.fahrer_id fahrerID,
  f.fahrername AS fahrer,
  v.hersteller AS auto
FROM team t
LEFT JOIN fahrer f ON f.team_id = t.team_id
LEFT JOIN rennergebnis re ON re.fahrer_id = f.fahrer_id
LEFT JOIN fahrzeuge v ON v.fahrzeug_id = re.fahrzeug_id
WHERE t.team_name = '{team_name_sql}'
ORDER BY f.fahrername
"""

    result = anvil.server.call('query_database', sql)
    print(result)
    
    self.repeating_panel_Team_daten.items = result
    