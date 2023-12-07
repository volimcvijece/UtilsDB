#todo: OCISTITI OD SQL INJECTIONA!!!!

#NAVESTI DA JE OVO ISKLJUCIVO ZA T-SQL!!!! #TODO

def select_all(table_fullpath, scope=''):
    #dodati sql injection cleaning!
    return f"""SELECT * FROM {table_fullpath} {scope};"""

def select_distinct_col(colname,table_fullpath):
    #dodati sql injection cleaning!
    return f"""SELECT DISTINCT {colname} FROM {table_fullpath} ;"""


def get_column_info_one_table_old(table_schema, table_name):
    #odluka - ne koristiti CHARACTER_MAXIMUM_LENGTH da uhvatim ako je nesto kropano! decimale... da? ali zato automatski za sve 
    #decimal i float i int baciti descriptor o min i max! (i castati naravno)
    #mozda da li neka is nullable kolona ima null iak one bi smjela by design

    query = f"""
     SELECT 
     --TABLE_CATALOG, 
     TABLE_SCHEMA,TABLE_NAME, COLUMN_NAME, IS_NULLABLE AS TARGET_IS_NULLABLE
    , DATA_TYPE AS TARGET_DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS TARGET_MAX_CHAR, NUMERIC_SCALE AS TARGET_DECIMAL_SCALE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{table_schema}'
    AND TABLE_NAME = '{table_name}'
        """
    
    return query

def get_column_info_one_table(databasename,table_schema, table_name):
    #odluka - ne koristiti CHARACTER_MAXIMUM_LENGTH da uhvatim ako je nesto kropano! decimale... da? ali zato automatski za sve 
    #decimal i float i int baciti descriptor o min i max! (i castati naravno)
    #mozda da li neka is nullable kolona ima null iak one bi smjela by design

    query = f"""
     SELECT 
     --TABLE_CATALOG, 
     TABLE_SCHEMA,TABLE_NAME, COLUMN_NAME, IS_NULLABLE AS TARGET_IS_NULLABLE
    , DATA_TYPE AS TARGET_DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS TARGET_MAX_CHAR, NUMERIC_SCALE AS TARGET_DECIMAL_SCALE
    --FROM serverinstance.{databasename}.INFORMATION_SCHEMA.COLUMNS
    FROM {databasename}.INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{table_schema}'
    AND TABLE_NAME = '{table_name}'
        """
    
    return query



def get_column_info_whole_db(databasename):
    #odluka - ne koristiti CHARACTER_MAXIMUM_LENGTH da uhvatim ako je nesto kropano! decimale... da? ali zato automatski za sve 
    #decimal i float i int baciti descriptor o min i max! (i castati naravno)
    #mozda da li neka is nullable kolona ima null iak one bi smjela by design

    #TODO - In general, INFORMATION_SCHEMA views should be avoided in favor of the catalog views introduced in SQL Server 2005 (and augmented since then). Why? Because the catalog views continue being developed as new features are added to SQL Server, while the info_schema views have not
    query = f"""
    SELECT 
    TABLE_CATALOG
    , TABLE_SCHEMA, TABLE_NAME
	,TABLE_SCHEMA+'.'+TABLE_NAME AS TABLENAMEFULL
    ,COLUMN_NAME, IS_NULLABLE AS TARGET_IS_NULLABLE
    , DATA_TYPE AS TARGET_DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS TARGET_MAX_CHAR, NUMERIC_SCALE AS TARGET_DECIMAL_SCALE
    ,ORDINAL_POSITION
    --FROM serverinstance.{databasename}.INFORMATION_SCHEMA.COLUMNS
    FROM {databasename}.INFORMATION_SCHEMA.COLUMNS
	WHERE TABLE_SCHEMA NOT IN ('ref','common');
    """
    
    return query

def get_column_info_whole_db_with_ref(databasename):
    #odluka - ne koristiti CHARACTER_MAXIMUM_LENGTH da uhvatim ako je nesto kropano! decimale... da? ali zato automatski za sve 
    #decimal i float i int baciti descriptor o min i max! (i castati naravno)
    #mozda da li neka is nullable kolona ima null iak one bi smjela by design

    #TODO - In general, INFORMATION_SCHEMA views should be avoided in favor of the catalog views introduced in SQL Server 2005 (and augmented since then). Why? Because the catalog views continue being developed as new features are added to SQL Server, while the info_schema views have not
    query = f"""
    SELECT 
    TABLE_CATALOG
    , TABLE_SCHEMA, TABLE_NAME
	,TABLE_SCHEMA+'.'+TABLE_NAME AS TABLENAMEFULL
    ,COLUMN_NAME, IS_NULLABLE AS TARGET_IS_NULLABLE
    ,ORDINAL_POSITION
    , DATA_TYPE AS TARGET_DATA_TYPE, CHARACTER_MAXIMUM_LENGTH AS TARGET_MAX_CHAR, NUMERIC_SCALE AS TARGET_DECIMAL_SCALE
    --FROM serverinstance.{databasename}.INFORMATION_SCHEMA.COLUMNS
    FROM {databasename}.INFORMATION_SCHEMA.COLUMNS
    """
    
    return query


def get_column_info_fk(table_name=None):

    #TODO - In general, INFORMATION_SCHEMA views should be avoided in favor of the catalog views introduced in SQL Server 2005 (and augmented since then). Why? Because the catalog views continue being developed as new features are added to SQL Server, while the info_schema views have not
 
    query=f"""
    SELECT
        FK_Table = FK.TABLE_NAME,
        FK_Column = CU.COLUMN_NAME,
        PK_Table = PK.TABLE_NAME,
        PK_Column = PT.COLUMN_NAME,
        Constraint_Name = C.CONSTRAINT_NAME,
		PT.CONSTRAINT_NAME AS Constraint_Name_PK
    FROM
        INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS C
    INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS FK
        ON C.CONSTRAINT_NAME = FK.CONSTRAINT_NAME
    INNER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS PK
        ON C.UNIQUE_CONSTRAINT_NAME = PK.CONSTRAINT_NAME
    INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE CU
        ON C.CONSTRAINT_NAME = CU.CONSTRAINT_NAME
    INNER JOIN (
                SELECT
                    i1.TABLE_NAME,
                    i2.COLUMN_NAME,
					i1.CONSTRAINT_NAME
                FROM
                    INFORMATION_SCHEMA.TABLE_CONSTRAINTS i1
                INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE i2
                    ON i1.CONSTRAINT_NAME = i2.CONSTRAINT_NAME
                WHERE
                    i1.CONSTRAINT_TYPE = 'PRIMARY KEY'
            ) PT
        ON PT.TABLE_NAME = PK.TABLE_NAME
    """
    if table_name:
        query+= f"WHERE FK.TABLE_NAME = '{table_name}'"
    
    return query


