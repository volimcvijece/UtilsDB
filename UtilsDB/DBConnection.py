import pyodbc
import pandas as pd
import numpy as np
import pymssql


# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)


def create_conn(server:str, database:str):
    conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                  'Server='+server+';'
                  'Database='+database+';'
                  'Trusted_Connection=yes;')

    return conn


def create_conn_pym(server:str, user:str, password:str, database:str):
    conn = pymssql.connect(server, user, password, database)
    return conn 

def get_cursor_dict(connection):
    return connection.cursor(as_dict=True)

#%% UVIJEK ZATVORITI KONEKCIJU ZA SQL SERVER!!!
def close_con(connection):
    connection.close()

# PANDAS SQL ALCH DOESN'T SUPPORT LINKED SERVERS
# UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy
#testdf = pd.read_sql_query(sqlcode, cnxn)
                      

#NIJE DOBRO JER DOBIJAM pri ponovnom pokretanju
# ProgrammingError: The cursor's connection has been closed.

#TODO - na oba dodati try except
def run_query_dict(connection,sqlcode):
    rows=[]
    try:
        cursor=connection.cursor(as_dict=True)
        cursor.execute(sqlcode) 
        #result = cursor.execute(sqlcode) #WORKS for pyodbc but not for pymsql
        #rows = result.fetchall() #WORKS for pyodbc but not for pymsql
        rows = cursor.fetchall()

    #while row: 
    #    print(row)
    #    row = cursor.fetchone()
    except Exception as e:
        print("Couldnt query the table, ", e)
    #columns = [column[0] for column in cursor.description]



    return rows


#only for DICT CURSOR!
def run_query(cursor, sqlcode):
    cols = []

    try:
        result = cursor.execute(sqlcode) #WORKS for pyodbc but not for pymsql
        rows = result.fetchall() #WORKS for pyodbc but not for pymsql
        rows = cursor.fetchall()

    #while row: 
    #    print(row)
    #    row = cursor.fetchone()
    except Exception as e:
        print("Couldnt query the table, ", e)
        return [], []
    #columns = [column[0] for column in cursor.description]

    if len(rows)>0:
        cols = list(rows[0].keys())
    
     #WORKS for pyodbc but not for pymsql
    for i,_ in enumerate(result.description): #WORKS for pyodbc but not for pymsql
        cols.append(result.description[i][0]) #WORKS for pyodbc but not for pymsql
    for row in cursor:
        cols.append(row)
    

    return rows, cols


def run_query_only_rows(cursor, sqlcode):
    try:
        result = cursor.execute(sqlcode) 
        rows = result.fetchall() #fetch all! pogledati dobre prakse
    #while row: 
    #    print(row)
    #    row = cursor.fetchone()
    except Exception as e:
        print("Couldnt query the table, ", e)
        return [] 
    #columns = [column[0] for column in cursor.description]
    return rows


##TEMP WORKAROUND- IN The FUTURE, EVERYTHING IN THE CLASS, SPECIFY ONLY THE PACKAGE
def run_query_to_df(cursor, sqlcode):
    rows, cols = run_query(cursor, sqlcode)
    if len(rows)==0:
        print(f'ERROR! Query returned empty table! Code: {sqlcode}')
        return []
    else:
        df = pd.DataFrame(np.array(rows), columns=cols)
        #df = pd.DataFrame(rows, columns=cols)
        return df

def run_query_to_df_temp(connection, sqlcode):
    rows = run_query_dict(connection, sqlcode)
    if len(rows)==0:
        print(f'ERROR! Query returned empty table! Code: {sqlcode}')
        return []
    else:
        df = pd.DataFrame(rows)
        #df = pd.DataFrame(rows, columns=cols)
        return df

