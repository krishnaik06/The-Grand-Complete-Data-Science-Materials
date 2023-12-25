import logging
import pyodbc
from datetime import datetime
from app.core.config import settings

class LogDBHandler(logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    pyodbc required
    '''
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        
        try:
            cnxn = pyodbc.connect(settings.CONNECTION_STRINGS)
            cursor = cnxn.cursor()

            sp_name = "{CALL exception_log (?,?,?,?)}"
            params = (datetime.utcnow().replace(microsecond=0), record.levelname, record.msg, record.name,)
            
            # Execute Stored Procedure With Parameters
            cursor.execute(sp_name, params)
            cnxn.commit()
            # Close the cursor and delete it
            cursor.close()
            del cursor
            
            # Close the database connection
            cnxn.close()
        except pyodbc.Error as ex:
            raise ex
