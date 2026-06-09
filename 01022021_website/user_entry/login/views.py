import random
from django.http import FileResponse
import matplotlib.font_manager as font_manager
from matplotlib import colors
from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from django.core import serializers
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . import Download_data
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
#from core.tokens import account_activation_token
import mimetypes
import csv
import base64
from io import BytesIO
import pandas as pd



from datetime import datetime
from functools import wraps

matplotlib.use('Agg')


# Decorator to prevent browser caching of authenticated pages
def no_cache(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


def opendatabase():
  try:
    connection = psycopg2.connect(user="postgres",password="Root@1234A",host="127.0.0.1",port="5432",database="netala_database")
    cursor = connection.cursor()
    return connection,cursor
  except Exception as e:
    print("THERE IS SOME PROBLEM",e)
  
  
connection,cursor=opendatabase()
  
def unique(list1):
  x = np.array(list1)
  return np.unique(x).tolist() 


def logout(request):
  global check, name
  check = ''
  name = ''
  return redirect('landing')
  

#23.10.2020

def f1(email):
    print('i have called')
    
    # Get user's tenant_id
    cursor.execute("SELECT tenant_id FROM user_list WHERE email_id=%s", (email,))
    tenant_result = cursor.fetchone()
    tenant_id = tenant_result[0] if tenant_result else None
    
    # 1. Generate Sensor Checkboxes
    query = "select distinct(sensor_type) from sensor_info order by sensor_type"   
    cursor.execute(query)
    node_records = cursor.fetchall()
    
    sensor = ""
    for row in node_records:
        for col in row:
            sensor_name = col.lower()
            icon = 'fa-microchip'
            if sensor_name == 'rain guage': icon = 'fa-cloud-rain'
            elif sensor_name == 'pitch': icon = 'fa-ruler-combined'
            elif sensor_name == 'pressure': icon = 'fa-tachometer-alt'
            elif sensor_name == 'voltage': icon = 'fa-bolt'
            elif sensor_name == 'rainfall': icon = 'fa-cloud-showers-heavy'
            elif sensor_name == 'vols': icon = 'fa-heartbeat'
            elif sensor_name == 'roll': icon = 'fa-sync-alt'
            elif sensor_name == 'moisture': icon = 'fa-tint'
            
            sensor += (
                f"<li><label class='styled-card' for='{col}'>"
                f"<div class='styled-card-content'>"
                f"<input class='styled-checkbox' id='{col}' name='st' type='checkbox' value='{col}'>"
                f"<i class='fas {icon} styled-icon'></i>"
                f"<span class='styled-text'>{col.upper()}</span>"
                f"</div>"
                f"</label></li>"
            )
            
    # Always prepend 'ALL' to the beginning of Sensor Types
    sensor = (
        "<li><label class='styled-card' for='allsen'>"
        "<div class='styled-card-content'>"
        "<input class='styled-checkbox' id='allsen' name='st' type='checkbox' value='all'>"
        "<i class='fas fa-layer-group styled-icon'></i>"
        "<span class='styled-text'>ALL</span>"
        "</div>"
        "</label></li>"
    ) + sensor
            
    # 2. Generate Location Checkboxes
    if tenant_id:
        query = "select node_id,location,name from node where tenant_id=%s"
        cursor.execute(query, (tenant_id,))
    else:
        query = "select node_id,location,name from node where node_id in (select node_id from node,u_status where node.location=u_status.location and email_id=%s)"
        cursor.execute(query, (email,))
    node_records = cursor.fetchall()
    
    import re
    def sort_node_key(row):
        name = row[2]
        match = re.search(r'\d+', name)
        return int(match.group()) if match else 9999
        
    node_records.sort(key=sort_node_key)
    
    location = ""
    state_name_for_map = "kerala" # Default fallback
    if tenant_id:
        cursor.execute("SELECT remarks FROM tenant WHERE tenant_id=%s", (tenant_id,))
        t_rem = cursor.fetchone()
        if t_rem and t_rem[0] and " for " in t_rem[0] and " Landslide" in t_rem[0]:
            state_name_for_map = t_rem[0].split(" for ")[1].split(" Landslide")[0].lower()
            
    for row in node_records:
        node_id, loc_name, name = row[0], row[1], row[2]
        location += (
            f"<li><label class='styled-card' for='{node_id}'>"
            f"<div class='styled-card-content'>"
            f"<input class='styled-checkbox' id='{node_id}' name='loc' type='checkbox' value='{node_id}'>"
            f"<i class='fas fa-map-marker-alt styled-icon'></i>"
            f"<span class='styled-text'>{loc_name.upper()}@{name.upper()}</span>"
            f"</div>"
            f"<i class='fas fa-chevron-right styled-arrow'></i>"
            f"</label></li>"
        )
        
    # Always prepend 'ALL' to the beginning of Locations, along with the state data
    location = (
        f"<input type='hidden' id='user_state_data' value='{state_name_for_map}'>"
        "<li><label class='styled-card' for='allloc'>"
        "<div class='styled-card-content'>"
        "<input class='styled-checkbox' id='allloc' name='loc' type='checkbox' value='all'>"
        "<i class='fas fa-th-large styled-icon'></i>"
        "<span class='styled-text'>ALL</span>"
        "</div>"
        "<i class='fas fa-chevron-right styled-arrow'></i>"
        "</label></li>"
    ) + location
        
    return sensor, location

def prepareQuery(word,data):
  content=word+' in ('
  for temp in data:
    content=content+'\''+temp+'\''+','
  content=content[:len(content)-1]
  content=content+')'
  return content

def f2():
  query="select email_id,uname from user_list where verify='yes' and status != 'accepted'"   
  cursor.execute(query)
  node_records = cursor.fetchall()
  if len(node_records)==0:
    s1="NO RECORD TO VALIDATE"
    return s1
  s1="<table border=1><tr><td>EMAIL</td><td>NAME</td><td>CLICK FOR YES</td></tr>"
  for row in node_records:
    s1=s1+"<tr><td>"+row[0]+"</td><td>"+row[1]+"</td> <td> <input type='checkbox' name='user' value='"+row[0]+"'></td></tr>"
  s1=s1+"</table>"
  return s1
  
def allow(request):
  s1=f2();
  return render(request,'allow.html',{'list':s1})

def insert(request):
  #print(request.POST)
  list_user=request.POST.getlist('user')
  global check
  check="credit"
  connection = psycopg2.connect(user="postgres",password="Root@1234A",host="127.0.0.1",port="5432",database="netala_database")
  cursor = connection.cursor()
  for item in list_user:
    query="update user_list set status='accepted' where email_id='"+item+"'"   
    print(query)
    cursor.execute(query)
    connection.commit()
  connection.close()
  cursor.close()
  return home(request,'web','<a href=allow.html>ALLOW USERS</a>')
  
  

@no_cache
def fetch_info(request):
  num1=[]
  num2=[]
  ty=request.POST['val']
  num1 = request.POST.getlist('st')
  num2 = request.POST.getlist('loc')

  if len(num1)==0 or len(num2)==0:
    sensor,location=f1(name)
    return render(request,'sensor-selection.html',{'sensor':sensor,'location':location,'user_name':name,'message_sp':"<font color='RED'>PLEASE SELECT THE VALUES </font>"})

  # Get user's tenant_id from user_list table
  tenant_query = "SELECT tenant_id FROM user_list WHERE email_id = %s"
  cursor.execute(tenant_query, (name,))
  tenant_result = cursor.fetchone()
  tenant_id = tenant_result[0] if tenant_result else None

  # Get user's allowed node_ids
  if tenant_id:
    allowed_nodes_query = "SELECT DISTINCT node_id FROM node WHERE tenant_id = %s"
    cursor.execute(allowed_nodes_query, (tenant_id,))
  else:
    allowed_nodes_query = """
      SELECT DISTINCT node.node_id FROM node
      INNER JOIN u_status ON node.location = u_status.location
      WHERE u_status.email_id = %s
    """
    cursor.execute(allowed_nodes_query, (name,))
  allowed_nodes_result = cursor.fetchall()
  allowed_node_ids = [row[0] for row in allowed_nodes_result]

  # If user selected 'all' locations, use all their allowed nodes
  if 'all' in num2:
    node_id = allowed_node_ids
  else:
    # Filter selected nodes to only include those the user has access to
    node_id = [n for n in num2 if n in allowed_node_ids]

  # If no valid nodes after filtering, show error
  if len(node_id) == 0:
    sensor,location=f1(name)
    return render(request,'sensor-selection.html',{'sensor':sensor,'location':location,'user_name':name,'message_sp':"<font color='RED'>NO VALID LOCATIONS SELECTED </font>"})

  # Build query for sensors filtered by tenant_id and allowed node_ids
  query = "SELECT DISTINCT sensor_id FROM sensor_info WHERE "
  conditions = []
  params = []

  # Filter by tenant_id
  if tenant_id:
    conditions.append("tenant_id = %s")
    params.append(tenant_id)

  # Filter by sensor type if not 'all'
  if len(num1) != 0 and 'all' not in [str(x).strip().lower() for x in num1]:
    type_placeholders = ','.join(['%s'] * len(num1))
    conditions.append("LOWER(TRIM(sensor_type)) IN (" + type_placeholders + ")")
    params.extend([str(item).strip().lower() for item in num1])

  # Filter by allowed node_ids
  if len(node_id) != 0:
    node_placeholders = ','.join(['%s'] * len(node_id))
    conditions.append("LOWER(TRIM(node_id)) IN (" + node_placeholders + ")")
    params.extend([str(item).strip().lower() for item in node_id])

  query += " AND ".join(conditions)
  cursor.execute(query, params)
  node_records = cursor.fetchall()


  sensor_id=[]
  for row in node_records:
    for col in row:
      sensor_id.append(col)

  import re
  def sort_sensor_key(s):
    s_upper = s.upper()
    n_match = re.search(r'_N(\d+)', s_upper)
    n_val = int(n_match.group(1)) if n_match else 9999
    
    type_order = 99
    if 'MS1' in s_upper: type_order = 1
    elif 'PH1' in s_upper: type_order = 2
    elif 'PRI' in s_upper or 'PR1' in s_upper: type_order = 3
    elif 'ROI' in s_upper or 'RO1' in s_upper: type_order = 4
    
    return (n_val, type_order, s_upper)

  sensor_id.sort(key=sort_sensor_key)

  sensor_id_list=""
  count=1
  for row in sensor_id:
    sensor_id_list += (
        f"<li><label class='styled-card' for='{row}'>"
        f"<div class='styled-card-content'>"
        f"<input class='styled-checkbox' id='{row}' name='sensor_list_id' type='checkbox' value='{row}'>"
        f"<span class='styled-text'>{row.upper()}</span>"
        f"</div>"
        f"</label></li>"
    )
  if ty=="app":
    return render(request,'inter.html',{'sensor_id':sensor_id_list,'hidden_value':'app'})

  return render(request,'sensor-data-selection.html',{
    'sensor_id':sensor_id_list,
    'hidden_value':'browser',
    'user_name': name if name else 'User'
  })


def index(request):
  # Landing page - check if user is logged in
  global check, name
  context = {'user_name': name if check == "credit" else None}
  return render(request,'index.html', context)

def login_form(request):
  return render(request,'login.html')

def register_form(request):
  cursor.execute("SELECT tenant_id, tenant_name, remarks FROM tenant WHERE is_active=true AND tenant_id != 1 ORDER BY tenant_id")
  tenants = cursor.fetchall()
  
  formatted_tenants = []
  for t in tenants:
      t_id = t[0]
      name = t[1]
      remark = t[2] if t[2] else ""
      
      if " for " in remark and " Landslide" in remark:
          state = remark.split(" for ")[1].split(" Landslide")[0]
          display_name = f"{state} ({name})"
      else:
          display_name = f"{name}"
          
      formatted_tenants.append({
          'id': t_id,
          'name': display_name
      })
      
  return render(request, 'register.html', {'tenants': formatted_tenants})




count_app=100

name=''
def login_page(request):
  global count_app
  global name
  global check

  # Handle GET request - show login form
  if request.method != 'POST':
    return redirect('signin')

  # Handle POST request - process login
  print(type(request.POST))
  name=request.POST['t11']
  print(name)
  password=request.POST['t12']
  print(password)
  status=request.POST['web']
  if request.POST.__contains__('count_app'):
   count_app=request.POST['count_app']

  query="select uname,email_id,user_type from user_list where(email_id='"+name+"' and upassword='"+password+"' and status='accepted')"
  try:
    cursor.execute(query)
    result=cursor.fetchall()
    print(len(result))
    if len(result) != 0:
      check="credit"
      if status == "app":
        sensor,location=f1(name)
        print("count_app",count_app)
        if count_app == "0":
          print("YESrt")
          count_app=10
          print(result[0][0]+"#"+result[0][1]+"#"+sensor+"#"+location)
          return HttpResponse(result[0][0]+"#"+result[0][1]+"#"+sensor+"#"+location);

        else:
          return redirect('home')
      else:
        # Redirect to home page (PRG pattern) instead of calling home() directly
        return redirect('home')
    else:
      if status =="app":
        return HttpResponse("credentials are not correct");     
      else:
        return render(request,'login.html',{'message':"credentials are not correct"})
      
  except Exception as e:
    print("ANY ERROR",e)
    if status == "web":
      return render(request,'login.html',{'message':"INVALID USER"})
    else:
      return HttpResponse("credentials are not correct"); 



check=""


@no_cache
def home(request,web=None,amessage=''):
  try:
    global check
    # Determine if request is from app or web browser
    # If web parameter not provided, check if it's a GET request (browser redirect)
    if web is None:
      web = "web" if request.method == "GET" else "app"
    print('in home',web)
    if check != "credit":
      # If not logged in, redirect to login page
      return redirect('signin')
    else:
       sensor,location=f1(name)
       print('i have come here ')
       print(sensor,location)
       if web=="app":
         print('last check')
         return render(request,'check.html',{'sensor':sensor,'location':location})
       else:
        print('new DATA',amessage)
        return render(request,'sensor-selection.html',{
          'sensor':sensor,
          'location':location,
          'user_name': name if name else 'User',
          'admin_message':amessage
        })
  except Exception as e:
    print('I AM IN EXCEPT',e)
    if web=="app":
      return HttpResponse("YOU ARE NOT A VALID USER..");
    else:
       return render(request,'login.html',{'message':"YOU ARE NOT A VALID USER......."})

def dateFix(date):
    if len(date) == 0:
      x = datetime.now()
      date = str(x)[0:10]
      print(date)
      return date
    else:
      return date


def dateFormat(request, date, x):
  from_hr = request.POST['from_hr']
  from_min = request.POST['from_min']
  to_hr = request.POST['to_hr']
  to_min = request.POST['to_min']
  if x=='f':
    format = str(date) + ' ' + from_hr + ':' + from_min + ':00'
  else:
    format = str(date) + ' ' + to_hr + ':' + to_min + ':00'
  print(date)
  return format


def queryExec(query):
  # print(query)
  cursor.execute(query)
  result = cursor.fetchall()
  return result


def preQuery(sensor_id):
  pre_query = "select distinct(sensor_type),sensor_id from sensor_info where "
  pre_query = pre_query + prepareQuery('sensor_id', sensor_id)
  node_records_pre = queryExec(pre_query)
  return node_records_pre


def prepQuery(charttype, sensor_id, to_format, from_format):
  if charttype == 'bar':
    query = "select sensor_data.sensor_id,avg(sensor_value),sensor_type from sensor_data,sensor_info where "
    if len(sensor_id) != 0:
      query = query + prepareQuery('sensor_data.sensor_id', sensor_id)
      query = query + ' and '
      query += "receive_time <= (to_timestamp('" + to_format + "','yyyy-mm-dd hh24:mi:ss')) and receive_time >= (to_timestamp('" + from_format + "', 'yyyy-mm-dd hh24:mi:ss'))"
      query = query + 'and sensor_data.sensor_id=sensor_info.sensor_id group by sensor_type,sensor_data.sensor_id order by sensor_type'
      return query
  else:
    print('Timeseries')

    query = "select sensor_data.sensor_id,sensor_value,RECEIVE_TIME,sensor_type from sensor_data,sensor_info  where sensor_data.sensor_id=sensor_info.sensor_id and "
    query_second = "select sensor_id,sensor_value,DATE_TRUNC('second',receive_time ) from sensor_data where (sensor_id,sensor_value) in ( select sensor_id  ,max(sensor_value) from sensor_data where "

    query = query + prepareQuery('sensor_data.sensor_id', sensor_id)
    query_second = query_second + prepareQuery('sensor_id', sensor_id)

    query = query + ' and '
    query_second = query_second + ' and '

    query += "receive_time < (to_timestamp('" + to_format + "','yyyy-mm-dd hh24:mi:ss')) and receive_time > (to_timestamp('" + from_format + "', 'yyyy-mm-dd hh24:mi:ss'))"
    query_second += "receive_time < (to_timestamp('" + to_format + "','yyyy-mm-dd hh24:mi:ss')) and receive_time > (to_timestamp('" + from_format + "', 'yyyy-mm-dd hh24:mi:ss'))"

    query = query + ' order by sensor_data.sensor_id,receive_time'
    query_second += 'group by sensor_id)'

    return query


dbtitle = ['voltage', 'pressure', 'roll', 'pitch', 'moisture']
ch_ytitle = ['Voltage (V)', 'Pressure (kPa)', 'Displacement (deg)', 'Displacement (deg)', 'Moisture (%)']


def ySet(x, li1, li2):
  for i in range(5):
    if x == li1[i]:
      x = li2[i]
  return x


def setData(records):
  data = []
  for row in records:
    data.append(row)
  return data


def sensorDict(data):
  Dict = {}
  Dict["sensorid"] = unique([row[0] for row in data])
  Dict["sensorid"].sort()
  Dict["sensorval"] = [row[1] for row in data]
  Dict["datelist"] = [row[2] for row in data]
  Dict["sensortype"] = unique([row[3] for row in data])
  return Dict


def getPre(records):
  ty = [row[0] for row in records]
  set_ty = set(ty)
  set_ty = list(ty)
  set_ty = sorted(ty)
  return set_ty


def tempData(table, sensor_id, row):
  flag = False
  y_temp = []
  for col in range(0, len(table)):
    if table[col][0] == sensor_id:
      countd = col
      #print(sensor_id, row)
      if table[col][3]=='pressure':
      #if sensor_id[row] == 'nt_n4_pr1' or sensor_id[row] == 'nt_n4_pr1_f' or sensor_id[row] == 'nt_n4_pr1_r' or \
              #sensor_id[row] == 'nt_n2_pr1_r' or sensor_id[row] == 'ng_n1_pr1':
        #change = ((float(table[countd][1]) / 1000 - 0.2) / 4.5) * 100
        change = (float(table[countd][1]))
        y_temp.append([table[countd][3], change, table[countd][2]])
        continue
     
      if table[col][3]=='moisture':
      #if sensor_id[row] == 'nt_n1_ms1' or sensor_id[row] == 'nt_n3_ms1' or sensor_id[row] == 'nt_n1_ms1_f':
        change = (73 - float(table[countd][1]))
        y_temp.append([table[countd][3], change, table[countd][2]])
        continue

      y_temp.append([table[countd][3], table[countd][1], table[countd][2]])

  return y_temp





def qThree(sensor_id):
  query = "select sensor_id, remark from sensor_info where "
  query = query + prepareQuery('sensor_id', sensor_id)
  return query


def labelDict(sensor_id):
  Dict = {}
  query = qThree(sensor_id)
  remark_Record = queryExec(query)
  for d in remark_Record:
    Dict[d[0]] = d[1]
  return Dict


def getPlotValues(data, pre, dic):
  for aa in data:
    if aa[0] == pre[0]:
      dic['oy'].append(aa[1])
      dic['ox'].append(aa[2])
    if len(pre) >= 2 and aa[0] == pre[1] and aa[0] != pre[0]:
      dic['ty'].append(aa[1])
      dic['tx'].append(aa[2])
    if len(pre) >= 3 and aa[0] == pre[2] and aa[0] != pre[0]:
      dic['thy'].append(aa[1])
      dic['thx'].append(aa[2])
  return dic


def get_graph(plot):
  buffer = BytesIO()
  plot.savefig('login/testplot.png')
  plot.savefig(buffer, format='png')
  buffer.seek(0)
  image_png = buffer.getvalue()
  graph = base64.b64encode(image_png)
  graph = graph.decode('utf-8')
  buffer.close()
  return graph


def firstPart(request):
  try:
    
    sensor_id = request.POST.getlist('sensor_list_id')
    from_date = request.POST['from_date']
    chart_type = request.POST['chart_type']
    to_date = request.POST['to_date']
    from_date = dateFix(from_date)
    from_format = dateFormat(request, from_date, 'f')
    to_date = dateFix(to_date)
    to_Format = dateFormat(request, to_date, 't')
    query = prepQuery(chart_type, sensor_id, to_Format, from_format)
    return query
  except:
    return None

def get_scientific_title(key):
  k = key.lower()
  if 'ms' in k or 'moisture' in k: return "Soil Moisture Variation"
  if 'pi' in k or 'pitch' in k: return "Pitch Angle Analysis"
  if 'pr' in k or 'pressure' in k: return "Pore Water Pressure Analysis"
  if 'ro' in k or 'roll' in k: return "Roll Sensor Monitoring"
  if 'rg' in k or 'rain' in k: return "Rainfall Trend"
  if 'vo' in k or 'voltage' in k: return "Voltage Monitoring"
  return f"Sensor Analysis: {key}"

def get_scientific_color(index):
  colors = ['#1f77b4', '#2E8B57', '#D62728', '#FF7F0E', '#9467BD']
  return colors[index % len(colors)]

@no_cache
def secondPartNew(request):
  global name
  Dict = {}
  Labels = {}
  plt.switch_backend('AGG')
  q = firstPart(request)
  node_records = queryExec(q)
  data = setData(node_records)
  sensor_id = request.POST.getlist('sensor_list_id')
  duration = request.POST['duration']
  try:
    from_date_str = request.POST.get('from_date', '').strip()
    to_date_str = request.POST.get('to_date', '').strip()
    from_date_str = dateFix(from_date_str)
    to_date_str = dateFix(to_date_str)
    import datetime as dt_mod
    from_date_obj = dt_mod.datetime.strptime(from_date_str, '%Y-%m-%d')
    to_date_obj = dt_mod.datetime.strptime(to_date_str, '%Y-%m-%d')
    days_diff = (to_date_obj - from_date_obj).days
      
    if str(duration) == "24" and days_diff > 25:
      duration = "168"
  except Exception as e:
    pass
  query_type=request.POST.get('query_type',None)
  Labels.update(labelDict(sensor_id))
  Dict.update(sensorDict(data))
  set_ty = getPre(preQuery(sensor_id))
  i = -1
  drawlist={}  

  for row in range(0, len(Dict["sensorid"])):
    i += 1
    fy, fx, sy, sx, ty, tx = ([] for _ in range(6))
    first_chartdic = {}
    first_chartdic['ox'] = fx
    first_chartdic['oy'] = fy
    first_chartdic['tx'] = sx
    first_chartdic['ty'] = sy
    first_chartdic['thx'] = tx
    first_chartdic['thy'] = ty
    Val = {}
    temp_data = tempData(data, Dict["sensorid"][i], row)
    Val.update(getPlotValues(temp_data, set_ty, first_chartdic))
    for aa in temp_data:
      dataset=drawlist.get(Dict["sensorid"][i],{})
      x=dataset.get('x',[])
      y=dataset.get('y',[])
      value=aa[0]
      y.append(aa[1])
      x.append(aa[2])
      drawlist[Dict["sensorid"][i]]={'x':x,'y':y,'value':value}
  keys=list(drawlist.keys())
  counter=0
  if query_type=="0":
    with BytesIO() as b:
      writer = pd.ExcelWriter(b, engine='xlsxwriter')
      for key in keys:
        data=drawlist[key]
        df=pd.DataFrame({'Time':data['x'],'values':data['y']})
        df.to_excel(writer, sheet_name=key)
      writer.close()
      filename = 'django_simple.xlsx'
      response = HttpResponse(
          b.getvalue(),
          content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      )
      response['Content-Disposition'] = 'attachment; filename=%s' % filename
      return response
  else:
    import json
    charts = []
    chart_index = 0
    for key in keys:
      data = drawlist[key]
      color = get_scientific_color(chart_index)
      
      raw_x = data['x']
      raw_y_list = []
      smoothed_y_list = []
      
      try:
        import pandas as pd
        raw_y = pd.to_numeric(pd.Series(data['y']), errors='coerce')
        
        window_size = max(3, min(len(raw_y) // 20, 48))
        if len(raw_y) > 5:
            smoothed_y = raw_y.rolling(window=window_size, center=True, min_periods=1).mean()
        else:
            smoothed_y = raw_y
            
        raw_y_list = [y if pd.notna(y) else None for y in raw_y]
        smoothed_y_list = [y if pd.notna(y) else None for y in smoothed_y]
      except:
        raw_y_list = data['y']
        smoothed_y_list = data['y']
      
      try:
        final_label = data['value'] + " (" + key + ")"
        raw_ylabel = ySet(final_label, key, key)
        if 'moisture' in raw_ylabel.lower() or 'ms' in key.lower(): unit = " (%)"
        elif 'pitch' in raw_ylabel.lower() or 'pi' in key.lower(): unit = " (°)"
        elif 'roll' in raw_ylabel.lower() or 'ro' in key.lower(): unit = " (°)"
        elif 'rain' in raw_ylabel.lower() or 'rg' in key.lower(): unit = " (mm)"
        elif 'pressure' in raw_ylabel.lower() or 'pr' in key.lower(): unit = " (kPa)"
        elif 'voltage' in raw_ylabel.lower() or 'vo' in key.lower(): unit = " (V)"
        else: unit = ""
        ylabel = raw_ylabel.split('(')[0].strip() + unit
      except:
        ylabel = key
        
      import datetime as dt_mod
      x_strings = []
      for dt in raw_x:
        if isinstance(dt, dt_mod.datetime):
            x_strings.append(dt.strftime('%Y-%m-%dT%H:%M:%S'))
        elif isinstance(dt, dt_mod.date):
            x_strings.append(dt.strftime('%Y-%m-%d'))
        else:
            x_strings.append(str(dt))
            
      charts.append({
          'id': key,
          'title': get_scientific_title(key),
          'raw_x': json.dumps(x_strings),
          'raw_y': json.dumps(raw_y_list),
          'smoothed_y': json.dumps(smoothed_y_list),
          'color': color,
          'duration': str(duration),
          'ylabel': ylabel
      })
      chart_index += 1
      
    # Calculate status level dynamically based on highest graph variance
    status_level = 1
    max_variance = 0
    global graph_danger_level
    try:
        import pandas as pd
        for key in keys:
            temp_data = drawlist[key]
            if len(temp_data['y']) > 0:
                raw_y = pd.to_numeric(pd.Series(temp_data['y']), errors='coerce').dropna()
                if len(raw_y) > 0:
                    y_max = raw_y.abs().max()
                    max_variance = max(max_variance, y_max)
        
        if max_variance > 80: status_level = 4
        elif max_variance > 50: status_level = 3
        elif max_variance > 20: status_level = 2
        else: status_level = 1
        
        graph_danger_level = status_level
    except Exception as e:
        print("Error calculating status level:", e)
        graph_danger_level = 1

    from datetime import datetime
    now = datetime.now()
    
    try:
        uname = name if name else 'User'
    except NameError:
        uname = 'User'
        
    try:
        import csv
        sensor_id_list = request.POST.getlist('sensor_list_id')
        from_date_str = request.POST['from_date']
        to_date_str = request.POST['to_date']
        from_date_fixed = dateFix(from_date_str)
        to_date_fixed = dateFix(to_date_str)
        from_format = dateFormat(request, from_date_fixed, 'f')
        to_Format = dateFormat(request, to_date_fixed, 't')
        
        csv_query = "SELECT * FROM sensor_data WHERE "
        csv_query += prepareQuery('sensor_id', sensor_id_list)
        csv_query += " AND receive_time <= (to_timestamp('" + to_Format + "','yyyy-mm-dd hh24:mi:ss')) AND receive_time >= (to_timestamp('" + from_format + "', 'yyyy-mm-dd hh24:mi:ss')) ORDER BY receive_time"
        
        cursor.execute(csv_query)
        csv_records = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        
        with open('data.csv', 'w+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(colnames)
            writer.writerows(csv_records)
    except Exception as e:
        print("Error generating full dataset CSV:", e)

    return render(request, 'data-visualization.html', {
      'charts': charts,
      'current_date': now.strftime('%B %d, %Y'),
      'current_time': now.strftime('%I:%M %p'),
      'user_name': uname
    })
  

        



      
  

def secondPart(request):

  Dict = {}
  Labels = {}
  plt.switch_backend('AGG')
  fig, ax = plt.subplots(figsize=(10,6))
  fig.subplots_adjust(right=0.75)

  flag=False
  flag1=False
  ab = True

  q = firstPart(request)
  node_records = queryExec(q)

  data = setData(node_records)
  sensor_id = request.POST.getlist('sensor_list_id')
  duration = request.POST['duration']

  Labels.update(labelDict(sensor_id))
  Dict.update(sensorDict(data))
  set_ty = getPre(preQuery(sensor_id))

  color_line = ['red', 'blue', 'green', 'black']
  markers = ['<', 'o', 'v', 'x', 'X', 'D', '|', '>', '+', '.', ',']

  i = -1

  # print(Labels)
  # print(data)
  # print(set_ty)

  for row in range(0, len(Dict["sensorid"])):
    # print('help')
    i += 1
    fy, fx, sy, sx, ty, tx = ([] for _ in range(6))
    first_chartdic = {}
    first_chartdic['ox'] = fx
    first_chartdic['oy'] = fy
    first_chartdic['tx'] = sx
    first_chartdic['ty'] = sy
    first_chartdic['thx'] = tx
    first_chartdic['thy'] = ty
    Val = {}
    # print('hello')
    temp_data = tempData(data, Dict["sensorid"][i], row)

    
    

    Val.update(getPlotValues(temp_data, set_ty, first_chartdic))

    for aa in temp_data:
      
      if aa[0] == set_ty[0]:
        fy.append(aa[1])
        fx.append(aa[2])
        flag = False

      if len(set_ty) >= 2 and aa[0] == set_ty[1]:
        sy.append(aa[1])
        sx.append(aa[2])
        flag = True
        flag1 = False

      if len(set_ty) >= 3 and aa[0] == set_ty[2]:  # only 3
        ty.append(aa[1])
        tx.append(aa[2])
        flag = True
        flag1 = True

    label = Labels[Dict["sensorid"][row]]
    # print('hekkio')
    # print(flag)
    formatter = mdates.DateFormatter("%d\n%m\n%Y")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.HourLocator(interval=int(duration))
    ax.xaxis.set_major_locator(locator)
    color_line = ['red', 'blue', 'green', 'black']
    p1, = ax.plot(fx, fy, label=label, color=color_line[i % 10], linewidth=.5, marker=markers[i % 6], markersize=.1)
    ax.set_xlabel('Time')
    ax.set_ylabel(ySet(set_ty[0],dbtitle,ch_ytitle))

    # print(set_ty)

    if len(set_ty) >= 2 and flag and ab:
      ax2 = ax.twinx()
      formatter = mdates.DateFormatter("%d\n%m\n%Y")
      ax2.xaxis.set_major_formatter(formatter)
      locator = mdates.HourLocator(interval=int(duration))
      ax2.xaxis.set_major_locator(locator)
      if len(sx) > 0:
        p2, = ax2.plot(sx, sy, label=label, color=color_line[i % 10], linewidth=.91, marker=markers[(6 - i) % 6],
                   markersize=.11)

        ax2.set_xlabel('Time')
        ax2.set_ylabel(ySet(set_ty[1], dbtitle, ch_ytitle))
      ab = False
      sx = []
      sy = []
      for tick in ax2.get_xticklabels():
        tick.set_rotation(60)
        tick.set_fontsize(10)
    if len(set_ty) >= 2 and flag and flag1:
       ax3 = ax.twinx()
       ax3.spines.right.set_position(("axes", 1.2))
       formatter = mdates.DateFormatter("%d\n%m\n%Y")
       ax3.xaxis.set_major_formatter(formatter)
       locator = mdates.HourLocator(interval=int(duration))
       ax3.xaxis.set_major_locator(locator)
       p3, =ax3.plot(tx, ty, label=label, color=color_line[i % 10], linewidth=.3, marker=markers[(6 - i) % 6],
                markersize=.1)

       ax3.set_xlabel('Time')
       ax3.set_ylabel(ySet(set_ty[2], dbtitle, ch_ytitle))
  if len(set_ty)<2:
    ax.legend(handles=[p1], loc='upper right')
  elif len(set_ty)<3 and len(set_ty)>2:
    ax.legend(handles=[p1, p2], loc='upper right')
  else:
    ax.legend(handles=[p1, p2, p3], loc='upper right')

  chart = get_graph(fig)
  if len(set_ty) == 1:
    with open('data.csv','w+',newline='') as file:
      writer = csv.writer(file)
      writer.writerows(data)
  else:
    csv_file = open('data.csv','w+')
    csv_file.close()
  return render(request, 'results.html', {'chart': chart})
  
def download(request):
  filename = "data.csv"
  filepath = "data.csv"
  try:
    csv_file = open(filepath, 'rb')
  except FileNotFoundError:
    return HttpResponse("Data file not generated yet. Please submit a data request first.", status=404)
    
  mime_type, _ = mimetypes.guess_type(filepath)
  response = HttpResponse(csv_file, content_type = mime_type)
  response['Content-Disposition'] = "attachment; filename = %s" %filename
  return response

def activate(request, uidb64, token):
  print('HAS CAME HERE')
  from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
  try:
    email = force_text(urlsafe_base64_decode(uidb64))
    signer = TimestampSigner()
    # Verify token, max age 1 day (86400 seconds)
    original_uidb64 = signer.unsign(token, max_age=86400)
    
    if uidb64 == original_uidb64:
      innerquery="update user_list set verify='yes' where email_id=%s"
      cursor.execute(innerquery, [email])
      connection.commit()
      return HttpResponse("Thank you for your email confirmation. Now you can login to your account after admin validation. <br><a href='/'>CLICK HERE TO HOME</a>")
    else:
      return HttpResponse("Activation link is invalid! <br><a href='/'>CLICK HERE TO RETURN</a>")
  except (SignatureExpired, BadSignature, TypeError, ValueError, OverflowError) as e:
    print('Activation Error:', e)
    return HttpResponse("Activation link is invalid or expired! <br><a href='/'>CLICK HERE TO RETURN</a>")  
         #190720950
         
         
         
def registration(request):
  global name
  global check
  try:
    full_name=request.POST['t1']
    password=request.POST['t3']
    ph_no=request.POST['t4']
    email=request.POST['t5']
    utype=request.POST['t6']
    tenant_id=request.POST['tenant_id']
    web=request.POST.get("web", "web")
  except KeyError as e:
    return render(request, 'register.html', {'message': f'Missing field: {str(e)}'})

  try:
    # Check if user already exists in user_list
    cursor.execute("SELECT uname FROM user_list WHERE uname = %s", [full_name])
    if cursor.fetchone():
        return render(request, 'register.html', {'message': 'Username already taken.'})
        
    cursor.execute("SELECT email_id FROM user_list WHERE email_id = %s", [email])
    if cursor.fetchone():
        return render(request, 'register.html', {'message': 'Email already registered.'})

    query="insert into user_list(uname, upassword, ph_no, email_id, user_type, status, verify, tenant_id) values(%s, %s, %s, %s, %s, 'accepted', 'yes', %s)"
    try:
        cursor.execute(query, [full_name, password, ph_no, email, utype, tenant_id])
        connection.commit()
    except Exception as db_e:
        # Fallback to original insert if column names are wrong
        connection.rollback()
        query="insert into user_list values(%s, %s, %s, %s, %s, 'accepted', 'yes', 1)"
        cursor.execute(query, [full_name, password, ph_no, email, utype])
        connection.commit()

    # Automatically log the user in
    name = email
    check = "credit"

    if web == "app":
      return HttpResponse(email + "#" + "SUCCESS" + "#" + "" + "#" + "")
    else:
      return redirect('home')
      
  except Exception as e:
    import traceback
    print('Registration Exception:', e)
    traceback.print_exc()
    if web == "app":
      return HttpResponse("Unable to create account at the moment. Please try again later.")
    else:
      return render(request, 'register.html', {'message': "Unable to create account at the moment. Please try again later."})
     



  #return HttpResponse("DATA HAS BEEN NOT SUBMITTED");


# New view functions for additional pages
def about(request):
    """Render the About Us page"""
    # Check if user is logged in by checking the global check variable
    global check, name
    context = {'user_name': name if check == "credit" else None}
    return render(request, 'about.html', context)

def mission(request):
    """Render the Mission page"""
    # Check if user is logged in by checking the global check variable
    global check, name
    context = {'user_name': name if check == "credit" else None}
    return render(request, 'mission.html', context)

def contact(request):
    """Render the Contact page"""
    # Check if user is logged in by checking the global check variable
    global check, name
    context = {'user_name': name if check == "credit" else None}
    return render(request, 'contact.html', context)

def coming_soon(request):
    """Render the Coming Soon page"""
    # Check if user is logged in by checking the global check variable
    global check, name
    context = {'user_name': name if check == "credit" else None}
    return render(request, 'coming-soon.html', context)

def team(request):
    """Render the Team page"""
    global check, name
    context = {'user_name': name if check == "credit" else None}
    return render(request, 'team.html', context)

def monitoring_page(request):
    """Render the Monitoring Scale page"""
    global check, name
    global graph_danger_level
    
    try:
        status_level = graph_danger_level
    except NameError:
        status_level = 1
        
    context = {
        'user_name': name if check == "credit" else None,
        'graph_status_level': status_level
    }
    return render(request, 'monitoring.html', context)
