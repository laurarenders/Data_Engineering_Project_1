from cProfile import run
import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder

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
    
    return pd.read_sql_query(sql, connection)

def dropConstraint():
    try:
        qry = (
            "ALTER TABLE Bedrijf"
            "DROP FOREIGN KEY BedrijfID"
        )

        run_query(qry)
    except:
        print('niet gelukt om key te droppen')


def resetBedrijf():
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE Bedrijf')
    cursor.close()

def addWebContent():
    qryKolomToevoegen = (
        "ALTER TABLE Bedrijf "
        "ADD gescrapeteData LONGTEXT;"
    )

    qryWebContentInlezen = (
        "LOAD DATA LOCAL INFILE 'C:/DEPGroep1/scores/data.csv' "
        "INTO TABLE Bedrijf "
        "FIELDS TERMINATED BY ';' "
        "LINES TERMINATED BY '\n' "
        "IGNORE 1 ROWS;"
        )
        
    try:
        cursor = connection.cursor()
        cursor.execute(qryWebContentInlezen)
        cursor.close()
        connection.commit()
    except:
        print('Niet gelukt')



open_ssh_tunnel()
mysql_connect()

# Gescrapete data doorvoeren naar de databank. 
# addWebContent()

# dropConstraint()
# resetBedrijf()

qry = run_query('select * from Bedrijf')
print(qry)