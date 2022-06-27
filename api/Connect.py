class Connect():
    def __init__(self, short_host_name, database=''):
        host, port, password = hosts.get(short_host_name)
        
        # for pandahouse
        self.pdh_conn = dict(host=f'http://{host}:{port}',
                            user=click_user,
                            password=password,
                            database=database)
        
        # for sqlalchemy
        self.alchemy_conn = f'clickhouse+http://{click_user}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(self.alchemy_conn)
        session = make_session(self.engine)
        
        # for mysql
        if short_host_name in ('mysql', 'tecdoc'):
            host, port, password = hosts.get(short_host_name)
            self.mysql_conn = pmsql.connect(host=host,
                                             port=int(port),
                                             user=mysql_user,
                                             passwd=password,
                                             db=database)
        
    # SELECTS
    
    def select_mysql(self, sql):
        return pd.read_sql_query(sql, self.mysql_conn)
    
    def select_alchemy(self, sql):
        connection = self.engine.connect()
        df = pd.read_sql_query(sql, self.engine)
        connection.close()
        return df
