import pyodbc
import pandas as pd
from app.core.config import settings

# Function to return the sql results as a dict. 
# It also maps the column names and values for the dict
# Returns no results found if there are no records
def convert_result2dict(cursor):
    try: 
        result = []
        columns = [column[0] for column in cursor.description]
        for row in  cursor.fetchall():
            result.append(dict(zip(columns,row)))

        #print(result)
        #Check for results
        if len(result) > 0:
            ret_result = result
        else:
            ret_result = None
    except pyodbc.Error as e:
        print(e)
        ret_result = None
    
    return ret_result

class token_dbcontext:

    def get_api_consumer_details(self, user_name):

        cnxn = pyodbc.connect(settings.CONNECTION_STRINGS)
        cursor = cnxn.cursor()

        sp_name = "{CALL getAPIConsumerDetails (?)}"
        params = (user_name,)
        
        # Execute Stored Procedure With Parameters
        cursor.execute(sp_name, params)

        result = convert_result2dict(cursor)
        
        # Close the cursor and delete it
        cursor.close()
        del cursor
        
        # Close the database connection
        cnxn.close()

        return result
