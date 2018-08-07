import psycopg2

def connect_rds(host, port, db_name, user, pwd):
    """
    Return RDS connection
    """
    kwargs = {
        "database": db_name,
        "user": user,
        "password": pwd,
        "host": host,
        "port": port
    }
    conn = psycopg2.connect(**kwargs)
    return conn

def _execute_single_query(conn, query, value_dict=None):
    """
    Usage for x in execute_single_query(conn, query):
              print(x)
    """
    cur = conn.cursor()
    if value_dict:
        cur.execute(query, value_dict)
    else:
        cur.execute(query)
    rows = cur.fetchall():
    for x in rows:
        yield x

def get_people_cooperation(conn, people_id1, people_id2):
    cur = conn.cursor()
    values = {}
    if people_id1 < people_id2:
        values['id1'] = people_id1
        values['id2'] = people_id2
    else:
        values['id1'] = people_id2
        values['id2'] = people_id1
    cur.execute("""
        SELECT PROJECT_NAME, DURATION
        FROM COOPERATION
        WHERE PEOPLE_ID1 = %(id1)s AND PEOPLE_ID2 = %(id1)s
        ORDER BY DURATION DESC
        """, values)
    rows = cur.fetchall()
    for x in rows:
        yield x

def get_cooperators(conn, people_id):
 