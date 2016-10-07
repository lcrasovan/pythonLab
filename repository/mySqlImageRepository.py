# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine

class MySqlImageRepository:  
    def __init__(self, connectionString):
        self.engine = create_engine(connectionString)
    
    def findImagesByQuery(self, query):
        return pd.read_sql_query(query,self.engine)
        
          