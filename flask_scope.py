from flask import Flask, request, Response, jsonify, make_response
from datetime import datetime, timezone
from time import sleep
import mariadb
import json
import subprocess
import ast
import threading


# from astropy.coordinates import EarthLocation, SkyCoord, AltAz
# from astropy import units as u
# from astropy.time import Time

# def radec_to_altaz(ra, dec, lat, lon, elev, time, frame='icrs'):
#     location = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=elev*u.m)
#     coords = SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame=frame)
#     if frame == 'icrs':
#         altaz_coords = coords.transform_to(AltAz(obstime=time, location=location))
#     else:
#         altaz_coords = coords.transform_to(AltAz(obstime=Time(time, format='jyear', scale='utc'), location=location))
#     return altaz_coords.alt.deg, altaz_coords.az.deg
# #initialize application
app = Flask(__name__)
#create the db connection to the camera DB

# cnx_cam = mysql.connector.connect(user='alpaca', password='dobri4',
#                               host='192.168.1.21',
#                               database='alpaca_camera')

#create the db connection to the scope DB


def monitor():
    while True:
        m_cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                                    host='192.168.1.21',
                                    database='alpaca_scope')
        m_cursor = m_cnx_scope.cursor()
        query = "SELECT name, value FROM properties where name in ('tracking','trackingrate','rightascension','declination','slewing','altitude','azimuth','rightascensionrate','declinationrate')"
        m_cursor.execute(query)
        value_row = m_cursor.fetchall()
        v_altitude = float(value_row[0][1])
        v_azimuth = float(value_row[1][1])
        v_declination = float(value_row[2][1])
        v_declinationrate = float(value_row[3][1])
        v_rightascension = float(value_row[4][1])
        v_rightascensionrate = float(value_row[5][1])
        v_slewing = value_row[6][1]
        v_tracking = value_row[7][1]
        v_trackingrate = value_row[8][1]
        m_cursor.close()
        m_cnx_scope.close()




        if v_slewing == 'True' :
            # print ('Calculated RA is ')
            out_rightascension=str(v_rightascension+(v_rightascensionrate/60/60))
            # print(out_rightascension)
            # print ('Ra rate is:')
            # print (v_rightascensionrate)
            # print ('Calculated DEC is ')
            out_declination=str(v_declination+(v_declinationrate/60/60))
            # print(out_declination)
        else:
            # print ("tracking is : "+v_tracking)
            if v_tracking == 'False':

                rightascension=v_rightascension-5*(15/360/60/60)
                if rightascension > 24 :
                    rightascension = rightascension -24
                elif rightascension < 0 :
                    rightascension = rightascension + 24
                out_rightascension=str(rightascension)

                declination = v_declination
                if declination > 90:
                    declination = 90


                out_declination=str(declination)

                # out_azimuth=str(out_azimuth)
                # out_altitude=str(v_altitude)
            else:
                out_rightascension=str(v_rightascension)
                out_declination=str(v_declination)
                # alt, az = radec_to_altaz(v_rightascension, v_declination,  42.689,23.2485, 502)
        alt= '10'
        az='20'
        out_azimuth = str (az)
        out_altitude = str (alt)

        m2_cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                                    host='192.168.1.21',
                                    database='alpaca_scope')
        m2_cursor = m2_cnx_scope.cursor()
        query = "update properties set value = '"+out_rightascension+"' where name = 'rightascension'"
        # print (query)
        m2_cursor.execute(query)
        query = "update properties set value = '"+out_declination+"' where name = 'declination'"
        # print (query)
        m2_cursor.execute(query)
        m2_cnx_scope.commit()
        m2_cursor.close()
        
        m2_cnx_scope.close()


        sleep(1)


@app.route('/api/test', methods=['GET','PUT'])
def test_api_call ():
    out_value = ast.literal_eval('[{\"Minimum\": \"0.1\", "Maximum":\"1.0\"}, {\"Minimum\": \"500.0\", \"Maximum\": \"10000.0\"}]')
    response_data = {'ClientTransactionID': 222 ,
                        'ServerTransactionID': 22,                                      
                        'ErrorNumber': 22,
                        'ErrorMessage': '',
                        'Value': out_value}
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    return make_response(jsonify(response_data), 200, headers)

@app.route('/api/v1/<in_device>/0/<in_action>', methods=['GET','PUT'])
def proccess_api_call(in_device, in_action):

    if in_device == 'telescope':
        cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                              host='192.168.1.21',
                              database='alpaca_scope')
        #Incretment v_server_transaction and get the new ID
        trans_cursor = cnx_scope.cursor()
        trans_query = "INSERT INTO `alpaca_scope`.`trasaction` (`id`) VALUES ( NULL);"
        trans_cursor.execute(trans_query)
        trans_query = "select MAX(id) from `alpaca_scope`.`trasaction`;"
        trans_cursor.execute(trans_query)
        trans_row = trans_cursor.fetchall()
        v_server_transaction = trans_row[0][0]
        trans_cursor.close()
        cnx_scope.commit()
        cnx_scope.close()
        #proccess GETs 
        if request.method == 'GET':
            cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
            host='192.168.1.21',
            database='alpaca_scope')
            action = in_action
            cursor = cnx_scope.cursor()
            query = "SELECT value, type, bash, python, get_parameter_name, get_parameter_type, get_parameter_name2, get_parameter_type2 FROM properties where name = ?"
            params= (action,)
            cursor.execute(query,params)
            value_row = cursor.fetchall()
            cursor.close()
            cnx_scope.commit()
            cnx_scope.close()
            error_num=0
            error_message=''
            if value_row[0][2] == 1:
                #run bash script
                out_value = ''
            
            elif value_row[0][3] == 1:
                #run pythong scrtipt to get the value
                if  action == 'utcdate':
                    out_value= datetime.utcnow()
                else:
                    out_value=''
            else:   
                if  str(value_row[0][4]) == 'Axis':
                    if action == 'canmoveaxis':
                        index=int(request.args.get('Axis'))
                        array_value = eval(str(value_row[0][0]))
                        out_value=  array_value[index]
                        
                    else :
                        index=int(request.args.get('Axis'))
                        array_value = ast.literal_eval(str("[{\"Minimum\": 0.1, \"Maximum\":1.0}, {\"Minimum\": 500.0, \"Maximum\": 10000.0}]"))
                        out_value=array_value
                        # print ('studpid value is : '+ str(out_value))
                        

                else:
                    if len(value_row) > 0:
                        type = value_row[0][1]
                        if type == 'bool':
                            if value_row[0][0] == 'True':
                                out_value = True
                            elif value_row[0][0] == 'False':
                                out_value = False
                            else:
                                out_value = False
                        elif type == 'int':
                            out_value = int(value_row[0][0])
                        elif type == 'double':
                            out_value = float(value_row[0][0])
                        elif type == 'intarray':
                            out_value = ast.literal_eval(str(value_row[0][0]))
                        elif type == 'dictarray':
                            out_value = ast.literal_eval(str(value_row[0][0]))
                        elif type == 'strarray':
                            out_value = ast.literal_eval(str(value_row[0][0]))
                        else:
                            out_value = value_row[0][0]
                    else:
                    # error_num=2
                        out_value=''
                    # error_message ='No parameter deffined'

            response_data = {'ClientTransactionID': request.args.get('ClientTransactionID',0) ,
                             'ServerTransactionID': v_server_transaction,                                      
                             'ErrorNumber': error_num,
                             'ErrorMessage': error_message,
                             'Value': out_value}
            headers = {'Content-Type': 'application/json;charset=utf-8'}

            return make_response(jsonify(response_data), 200, headers)
        
        # Proccess puts
        elif request.method == 'PUT':
            action = in_action

            cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
            host='192.168.1.21',
            database='alpaca_scope')
            cursor = cnx_scope.cursor()
            query = "SELECT id,name,type,value,isconstant, canget, canput, put_parameter_name, put_parameter_type,put_parameter_name2, put_parameter_type2 FROM properties where name = ?"
            params= (action,)
            cursor.execute(query,params)
            value_row = cursor.fetchall()
            cursor.close()
            cnx_scope.commit()
            cnx_scope.close()

            v_id = value_row[0][0]
            v_name = value_row[0][1]
            v_type = value_row[0][2]
            v_value = value_row[0][3]
            v_isconstant =  value_row[0][4]
            v_canputd = value_row[0][6]
            v_put_parameter_name = value_row[0][7]
            v_put_parameter_type = value_row[0][8]
            v_put_parameter_name2 = value_row[0][9]
            v_put_parameter_type2 = value_row[0][10]
            print ('Parameter Name: '  + str(v_put_parameter_name))
            print ('Parameter Value: '+ str(request.form.get(v_put_parameter_name)))
            print ('Parameter Name2: '  + str(v_put_parameter_name2))
            print ('Parameter Value2: '+ str(request.form.get(v_put_parameter_name2)))            
            #call shell for proccessing 
            subprocess.run(['/bin/bash',
                            'bash_scripts_scope/put_'+v_name+'.sh', 
                            str(v_type),
                            str(v_value),
                            str(in_action), 
                            str(v_put_parameter_type),
                            str(request.form.get(v_put_parameter_name)),
                            str(request.form.get(v_put_parameter_name2))
                                ])
            
            response_data = {'ClientTransactionID': request.form.get('ClientTransactionID',0) ,
                             'ServerTransactionID': v_server_transaction,                                      
                             'ErrorNumber': 0,
                             'ErrorMessage': ''}
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            print (response_data)
            print (headers)
            return make_response(jsonify(response_data), 200, headers)
   
    else:
        # some error for not existing device!
        return 
    


if __name__ == '__main__':
    thread = threading.Thread(target=monitor)
    thread.start()
    app.run(host='192.168.1.21', port=5000, debug=False)
