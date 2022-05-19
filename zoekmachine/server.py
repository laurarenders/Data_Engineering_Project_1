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
  query = f'SELECT b.Naam, b.Ondernemingsnummer, l.gemeente FROM Bedrijf b JOIN Locatie l ON b.Locatie = l.LocatieID WHERE b.Naam LIKE "{bedrijf}%" ORDER BY b.Naam, b.Ondernemingsnummer;'
  result = run_query(query)
  bedrijfsnamen = []
  gemeentes = []
  ondernemingsnummers = []

  # print(result)
  
  for r in result:
    bn = list(r)
    print(f"bn: {bn}")
    bedrijfsnamen.append([ord(b) for b in bn[0]])
    ondernemingsnummers.append(r[1])
    gem = list(r[2])
    gemeentes.append([ord(g) for g in gem])


  ls = [bedrijfsnamen, gemeentes, ondernemingsnummers]

  return render_template("bedrijfslijst.html", response = ls)

@app.route("/gedetailleerd.html")
def companyinfo():

  open_ssh_tunnel()
  mysql_connect()

  bedrijf = request.args.get("bedrijf")
  query = f'''SELECT b.Naam, s.Sector, b.Ondernemingsnummer, l.postcode, l.gemeente, b.Adres, b.AantalWerknemers, b.Omzet, b.Balanstotaal, b.Framework, b.SoortBusiness
            FROM Bedrijf b 
            JOIN Sector s ON b.sectorID = s.SectorID 
            JOIN Locatie l ON b.Locatie = l.LocatieID
            WHERE b.Naam = "{bedrijf}"
            ORDER BY b.Naam ASC;'''
  result = run_query(query)

  bedrijfsinfo = []

  for r in result[0]:
    print(r)
    if type(r) != int:
      bedrijfsinfo.append([ord(i) for i in r])
    else:
      bedrijfsinfo.append([r])

  print(bedrijfsinfo)

  return render_template("gedetailleerd.html", response=bedrijfsinfo)

@app.route("/perSector.html")
def perSector():
  return render_template("perSector.html")

@app.route("/sectorlijst.html")
def sectors():

  open_ssh_tunnel()
  mysql_connect()

  sector = request.args.get("sectoren")
  if sector != "/all":
    query = f'SELECT s.Sector FROM Sector s WHERE s.Sector LIKE "{sector}%" ORDER BY s.Sector ASC;'
  else:
    query = f'SELECT s.Sector FROM Sector s ORDER BY s.Sector ASC;'

  result = run_query(query)

  sectoren = []

  for r in result:
    se = r[0]
    sectoren.append([ord(s) for s in se])

  return render_template("sectorlijst.html", response=sectoren)

@app.route("/sectorOverzicht.html")
def sectorinfo():

  open_ssh_tunnel()
  mysql_connect()

  sector = request.args.get("sector")
  query = f'''SELECT b.Naam, b.Ondernemingsnummer, l.gemeente 
              FROM Bedrijf b 
              JOIN Locatie l ON b.Locatie = l.LocatieID
              WHERE (SELECT SectorID FROM Sector s WHERE Sector = "{sector}") = b.sectorID
              ORDER BY b.Naam ASC;'''
  result = run_query(query)
  bedrijfsnamen = []
  gemeentes = []
  ondernemingsnummers = []

  for r in result:
    bn = list(r[0])

    bedrijfsnamen.append([ord(b) for b in bn])
    ondernemingsnummers.append(r[1])
    gem = list(r[2])
    gemeentes.append([ord(g) for g in gem])


  ls = [bedrijfsnamen, gemeentes, ondernemingsnummers]

  return render_template("sectorOverzicht.html", response = ls)

if __name__ == '__main__':
    app.run(debug=True)