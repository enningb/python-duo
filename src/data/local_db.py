from sqlalchemy import create_engine
from duodata.settings import data_dir

local_db = create_engine('sqlite:///%s/duodata_data.db' % data_dir)
