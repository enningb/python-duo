from sqlalchemy import create_engine
from duo.settings import duo_data_dir

local_db = create_engine('sqlite:///%s/duo_data.db' % duo_data_dir)