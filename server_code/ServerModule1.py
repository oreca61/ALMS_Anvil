import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database(query: str):
  with sqlite3.connect(data_files["ALMS.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_database_dict(query: str):
  with sqlite3.connect(data_files["ALMS.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def hole_fahrer_plot_daten():
  conn = sqlite3.connect("/mnt/data/ALMS.db")
  cursor = conn.cursor()

  query = """
  SELECT 
      f.fahrername,
      r.strecke,
      r.datum,
      re.punkte
  FROM rennergebnis re
  JOIN fahrer f ON re.fahrer_id = f.fahrer_id
  JOIN rennen r ON re.renn_id = r.renn_id
  ORDER BY r.datum, f.fahrername
  """

  cursor.execute(query)
  rows = cursor.fetchall()
  conn.close()

  daten = defaultdict(lambda: {"rennen": [], "punkte": []})

  for fahrername, strecke, datum, punkte in rows:
    rennen_label = f"{strecke} ({datum})"
    daten[fahrername]["rennen"].append(rennen_label)
    daten[fahrername]["punkte"].append(punkte)

  return dict(daten)
