from flask import Flask, render_template, request, jsonify
import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

ssh_host = "vichogent.be"
ssh_username = "root"
ssh_password = "DEPGroep1"
database_username = "root"
database_password = "DEPGroep1"
database_name = "DEP1DatabaseV3" 
localhost = '127.0.0.1'

def open_ssh_tunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.
    
    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    """
    
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    
    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 40010),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )
    
    tunnel.start()

def mysql_connect():
    """Connect to a MySQL server using the SSH tunnel connection
    
    :return connection: Global MySQL database connection
    """
    
    global connection
    
    connection = pymysql.connect(
        host='127.0.0.1',
        user=database_username,
        passwd=database_password,
        db=database_name,
        port=tunnel.local_bind_port,
        local_infile=True
    )

def run_query(sql):
    """Runs a given SQL query via the global database connection.
    
    :param sql: MySQL query
    :return: Pandas dataframe containing results
    """
    cur = connection.cursor()
    cur.execute(sql)
    return cur.fetchall()
    # return pd.read_sql_query(sql, connection)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/bedrijfslijst.html")
def companies():

  open_ssh_tunnel()
  mysql_connect()

  bedrijf = request.args.get("bedrijven")
  # query = f"SELECT b.Naam, l.gemeente, b.Ondernemingsnummer FROM Bedrijf b JOIN Locatie l ON b.BedrijfID = l.BedrijfID WHERE b.Naam LIKE '%{bedrijf}%';"
  query = f"SELECT b.Naam, b.Ondernemingsnummer FROM Bedrijf b WHERE b.Naam LIKE '%{bedrijf}%';"
  result = run_query(query)
  bedrijfsnaam = ""
  bedrijfsnamen = []
  ondernemingsnummers = []

  for r in result:
    bn = list(r[0])

    bedrijfsnamen.append([ord(b) for b in bn])
    ondernemingsnummers.append(r[1])

  ls = [bedrijfsnamen,ondernemingsnummers]

  return render_template("bedrijfslijst.html", response = ls)

@app.route("/gedetailleerd.html")
def companyinfo():

  open_ssh_tunnel()
  mysql_connect()

  bedrijf = request.args.get("bedrijf")
  print(bedrijf)
  query = f"""SELECT b.Naam, s.Sector, b.Ondernemingsnummer, b.Adres, l.gemeente, tok.AantalWerknemers, tok.Omzet, tok.Balanstotaal, tok.Framework, tok.SoortBusiness, mb.score
            FROM Bedrijf b 
            JOIN Sector s ON b.sectorID = s.SectorID 
            JOIN Locatie l ON b.BedrijfID = l.LocatieID
            JOIN tempOrganisatorischeKenmerken tok ON b.BedrijfID = tok.BedrijfID
            JOIN milieuBeleid mb ON b.BedrijfID = mb.BedrijfID
            WHERE b.Naam = '{bedrijf}';"""
  result = run_query(query)
  bedrijfsnaam = ""
  bedrijfsnamen = []
  ondernemingsnummers = []

  for r in result:
    bn = list(r[0])

    bedrijfsnamen.append([ord(b) for b in bn])
    ondernemingsnummers.append(r[1])

  ls = [bedrijfsnamen,ondernemingsnummers]  # Nog in lijst zetten en doorgeven aan js

  return render_template("gedetailleerd.html")

@app.route("/perSector.html")
def perSector():
  return render_template("perSector.html")

@app.route("/sectorlijst.html")
def sectors():

  open_ssh_tunnel()
  mysql_connect()

  sector = request.args.get("sectoren")
  # query = f"SELECT b.Naam, l.gemeente, b.Ondernemingsnummer FROM Bedrijf b JOIN Locatie l ON b.BedrijfID = l.BedrijfID WHERE b.Naam LIKE '%{bedrijf}%';"
  query = f"SELECT s.Sector FROM Sector s WHERE s.Sector LIKE '%{sector}%';"
  result = run_query(query)

  sectoren = []

  for r in result:
    se = r[0]
    sectoren.append([ord(s) for s in se])

  print(sectoren)


  return render_template("sectorlijst.html", response=sectoren)

@app.route("/sectorGedetailleerd.html")
def sectorinfo():

  # open_ssh_tunnel()
  # mysql_connect()

  # bedrijf = request.args.get("sector")
  # print(bedrijf)
  # query = f"""Nog te maken"""
  # result = run_query(query)
  # bedrijfsnaam = ""
  # bedrijfsnamen = []
  # ondernemingsnummers = []

  # for r in result:
  #   bn = list(r[0])

  #   bedrijfsnamen.append([ord(b) for b in bn])
  #   ondernemingsnummers.append(r[1])

  # ls = [bedrijfsnamen,ondernemingsnummers]  # Nog in lijst zetten en doorgeven aan js

  return render_template("sectorGedetailleerd.html")

if __name__ == '__main__':
    app.run(debug=True)