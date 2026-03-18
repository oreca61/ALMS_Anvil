import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import random

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
def hole_fahrer_endstand():
  
  with sqlite3.connect(data_files["ALMS.db"]) as conn:
    
    cursor = conn.cursor()

    query = """
        SELECT f.fahrername, SUM(re.punkte) AS gesamtpunkte
        FROM rennergebnis re
        JOIN fahrer f ON re.fahrer_id = f.fahrer_id
        GROUP BY f.fahrer_id, f.fahrername
        ORDER BY gesamtpunkte DESC
        """

    cursor.execute(query)
    rows = cursor.fetchall()

  fahrer = []
  punkte = []

  for name, gesamtpunkte in rows:
    fahrer.append(name)
    punkte.append(gesamtpunkte)

  return {
    "fahrer": fahrer,
    "punkte": punkte
  }



@anvil.server.callable
def hole_fahrer_verlauf():
  with sqlite3.connect(data_files["ALMS.db"]) as conn:
    cursor = conn.cursor()

    query = """
        SELECT 
            f.fahrername,
            r.renn_id,
            r.strecke,
            re.punkte
        FROM rennergebnis re
        JOIN fahrer f ON re.fahrer_id = f.fahrer_id
        JOIN rennen r ON re.renn_id = r.renn_id
        ORDER BY r.renn_id ASC, f.fahrername ASC
        """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Alle Rennen in richtiger Reihenfolge sammeln
  rennen_reihenfolge = []
  for _, renn_id, strecke, _ in rows:
    label = f"R{renn_id}"
    if label not in rennen_reihenfolge:
      rennen_reihenfolge.append(label)

    # Punkte pro Fahrer pro Rennen sammeln
  fahrer_daten = {}

  for fahrername, renn_id, strecke, punkte in rows:
    label = f"R{renn_id}"

    
    if fahrername not in fahrer_daten:
      fahrer_daten[fahrername] = {
        "rennen": [],
        "punkte_pro_rennen": []
      }

    fahrer_daten[fahrername]["rennen"].append(label)
    
    fahrer_daten[fahrername]["punkte_pro_rennen"].append(punkte)


  result = {}

  
  for fahrername, daten in fahrer_daten.items():
    kumulativ = []
    
    gesamt = 0

    for p in daten["punkte_pro_rennen"]:
      gesamt += p
      
      kumulativ.append(gesamt)


      

    result[fahrername] = {
      "rennen":  daten["rennen"] ,
      
      "punkte":kumulativ
      
    }

    

  return result



@anvil.server.callable
def hole_random_news():
  
  with sqlite3.connect(data_files["ALMS.db"]) as conn:

    
    cursor = conn.cursor()
    
    news_liste = []


    
    cursor.execute("""
            SELECT f.fahrername, SUM(rg.punkte) AS gesamtpunkte
            FROM rennergebnis rg
            JOIN fahrer f ON rg.fahrer_id = f.fahrer_id
            GROUP BY f.fahrer_id, f.fahrername
            ORDER BY gesamtpunkte DESC
            LIMIT 1
        """)

    
    row = cursor.fetchone()

    
    if row is not None:
      news_liste.append(f"{row[0]} ist aktuell der beste Fahrer mit {row[1]} Punkten.")

      # Fahrer mit den meisten Siegen
    cursor.execute("""
            SELECT f.fahrername, COUNT(*) AS siege
            FROM rennergebnis rg
            JOIN fahrer f ON rg.fahrer_id = f.fahrer_id
            WHERE rg.platzierung = 1
            GROUP BY f.fahrer_id, f.fahrername
            ORDER BY siege DESC
            LIMIT 1
        """)
    row = cursor.fetchone()
    if row is not None:
      news_liste.append(f"{row[0]} hat die meisten Siege: {row[1]}.")

      # Hersteller mit den meisten Siegen
    cursor.execute("""
            SELECT fa.hersteller, COUNT(*) AS siege
            FROM rennergebnis rg
            JOIN fahrzeuge fa ON rg.fahrzeug_id = fa.fahrzeug_id
            WHERE rg.platzierung = 1
            GROUP BY fa.hersteller
            ORDER BY siege DESC
            LIMIT 1
        """)
    
    row = cursor.fetchone()
    
    if row is not None:
      news_liste.append(f"{row[0]} hat die meisten Siege: {row[1]}.")


    
    cursor.execute("""
            SELECT f.fahrername, COUNT(*) AS podien
            FROM rennergebnis rg
            JOIN fahrer f ON rg.fahrer_id = f.fahrer_id
            WHERE rg.platzierung <= 3
            GROUP BY f.fahrer_id, f.fahrername
            ORDER BY podien DESC
            LIMIT 1
        """)

    
    row=cursor.fetchone()


    
    if row is not None:
      news_liste.append(f"{row[0]} hat die meisten Podestplätze: {row[1]}.")

  
  if len(news_liste) ==0:
    return "Keine News verfügbar."


  
  return random.choice(news_liste)