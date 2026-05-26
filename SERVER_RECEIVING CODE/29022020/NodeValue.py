# This is the latest code till 28/02/2020
from Sensorinformation import Sensorinformation
import os
import sys
import psycopg2
from psycopg2 import pool as _pg_pool
from datetime import datetime
from contextlib import contextmanager
import random
import threading
import Send

DB_USER = "postgres"
DB_PASSWORD = "Root@1234A"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "netala_database"

# Thread lock for print calls to prevent interleaved/garbled output across threads
_print_lock = threading.Lock()


def _log(msg):
  """Thread-safe log for NodeValue."""
  with _print_lock:
    print('[%s] %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg), flush=True)


# Module-level connection pool. Each worker checks out a connection,
# does its DB work, and returns it. Replaces the previous single shared
# connection + global _db_lock — real parallelism is now possible up to maxconn.
#
# Timeouts and TCP keepalives prevent libpq from blocking forever:
#   - connect_timeout    : cap on initial psycopg2.connect() (was unbounded)
#   - statement_timeout  : PG server-side cancels any query > 10s
#   - keepalives_*       : detect a silently dropped TCP socket within ~60s
_DB_POOL = _pg_pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=16,
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME,
    connect_timeout=5,
    keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=3,
    options='-c statement_timeout=10000',
)


@contextmanager
def _db_conn():
  """Check out a connection from the pool. On exception, the connection is
  closed and discarded so the pool replaces it on next getconn()."""
  conn = _DB_POOL.getconn()
  bad = False
  try:
    yield conn
  except Exception:
    bad = True
    raise
  finally:
    try:
      if bad:
        try:
          conn.rollback()
        except Exception:
          pass
      _DB_POOL.putconn(conn, close=bad)
    except Exception:
      pass


def shutdown_pool():
  """Close all pooled connections. Called from Net.py on shutdown."""
  try:
    _DB_POOL.closeall()
  except Exception as e:
    _log('[WARN] pool closeall failed: %s' % e)


class ContentFromClient:
  a = 20

  def __init__(self, content, receive_time=None):
    self.content = content.lower()
    self.receive_time = receive_time or datetime.now()

  def get_node_id(self, cur, cname, name, tenantId):
    try:
      query = "SELECT node_id FROM node WHERE name=%s AND location=%s AND tenant_id=%s"
      cur.execute(query, (name, cname, tenantId))
      node_records = cur.fetchall()
      if not node_records:
        return None
      return node_records[0][0]
    except Exception as e:
      _log("[ERROR] Node ID lookup failed: %s" % e)
      return None

  def getTotalNodes():
    for i in content:
      pass

  def getTenantId(self):
    return "2"

  def getlocationName(self):
    indexofname = self.content.find('@')
    name = self.content[0:indexofname]
    self.content = self.content[indexofname + 1:]
    return name

  def getCordinatorName(self):
    indexofname = self.content.find('@')
    name = self.content[0:indexofname]
    self.content = self.content[indexofname + 1:]
    return name

  def getNodeName(self):
    indexofname = self.content.find('(')
    name = self.content[0:indexofname]
    self.content = self.content[indexofname:]
    return name

  def sensorvalues(self):
    tenantId = self.getTenantId()
    temp = self.getlocationName()
    coordinator_name = self.getCordinatorName()
    node_name = self.getNodeName()
    _log('[PROCESS] %s > %s | tenant=%s | pi_time=%s' % (coordinator_name, node_name, tenantId, self.receive_time))

    # Phase 1: parse sensor readings out of self.content. Pure CPU work,
    # no DB connection held. Threshold-breach SMTP threads fire here.
    records_to_parse = []  # list of (id_or_None, value, sensor_type, name)
    index = self.content.find(')', 1)
    value = ''
    while index != -1:
      id = ''
      temp = self.content[1:index]

      if temp.startswith('pressure'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'presure', coordinator_name)
        if _safe_float(value) >= 20000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'Presure VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('pr' + name[-1], value))

      elif temp.startswith('moisture'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'moisture', coordinator_name)
        if _safe_float(value) >= 50000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'MOISTURE VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('ms1', value))

      elif temp.startswith('roll'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'roll', coordinator_name)
        if _safe_float(value) >= 20000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'Roll VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('ro' + name[-1], value))

      elif temp.startswith('voltage'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'voltage', coordinator_name)
        if _safe_float(value) >= 20000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'Roll VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('voltage' + name[-1], value))

      elif temp.startswith('vols'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'vols', coordinator_name)
        if _safe_float(value) >= 20000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'Roll VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('vols' + name[-1], value))

      elif temp.startswith('pitch'):
        indexofcolon = self.content.find(':')
        name = self.content[1:indexofcolon]
        value = self.content[indexofcolon + 1:index]
        self.content = self.content[index + 1:]
        s = Sensorinformation(name, value, 'pitch', coordinator_name)
        if _safe_float(value) >= 2000:
          threading.Thread(target=Send.send_msg, args=('lews.sailab@gmail.com', 'rjvkmr80@gmail.com', 'PITCH VALUE IS CROSSING THRESOLD ' + value), daemon=True).start()
        records_to_parse.append(('pi' + name[-1], value))

      index = self.content.find(')', 1)

    # Phase 2: check out a pooled connection and do node_id lookup + inserts + commit.
    # Connection is held only for the DB work, not for parsing.
    try:
      with _db_conn() as conn:
        with conn.cursor() as cur:
          node_id = self.get_node_id(cur, coordinator_name, node_name, tenantId)
          if node_id is None:
            _log('[SKIP] Unknown node: %s @ %s' % (node_name, coordinator_name))
            return

          records_to_insert = []
          for suffix, val in records_to_parse:
            if val == "nan" or val == '':
              continue
            records_to_insert.append(('%s_%s' % (node_id, suffix), val, self.receive_time, tenantId))

          if records_to_insert:
            postgres_insert_query = 'INSERT INTO sensor_data (sensor_id,sensor_value,receive_time,tenant_id) VALUES (%s,%s,%s,%s)'
            cur.executemany(postgres_insert_query, records_to_insert)
            conn.commit()
            _log('[DB] Inserted %d records for %s > %s' % (len(records_to_insert), coordinator_name, node_name))
    except Exception as e:
      _log('[ERROR] DB insert failed: %s' % e)


def _safe_float(s):
  try:
    return float(s)
  except (ValueError, TypeError):
    return 0.0


if __name__ == "__main__":
  print('hi')
  # Test with explicit receive_time (simulating Pi timestamp)
  c = ContentFromClient("2@c1@kerala@n1(moisture1:581.02)(pitch10:-75)(roll1:-4)(pitch2:-95)(roll2:-95)(pitch3:-95)(roll3:-95)(pitch4:-95)(roll4:-95)", datetime.now())
  c.sensorvalues()
  shutdown_pool()
  print('DONE')
