from flask import Flask, request, Response, jsonify, make_response
from datetime import datetime, timezone
from time import sleep
import mariadb
import json
import subprocess
import ast
import threading    
import imageio_ffmpeg as ffmpeg
import numpy as np
from PIL import Image
import libraw
import rawpy
from json import JSONEncoder
import pickle
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
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)



@app.route('/api/v1/<in_device>/0/<in_action>', methods=['GET','PUT'])
def proccess_api_call(in_device, in_action):

    if in_device == 'camera':
        cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                              host='192.168.1.21',
                              database='alpaca_camera')
        #Incretment v_server_transaction and get the new ID
        trans_cursor = cnx_scope.cursor()
        trans_query = "INSERT INTO `alpaca_camera`.`trasaction` (`id`) VALUES ( NULL);"
        trans_cursor.execute(trans_query)
        trans_query = "select MAX(id) from `alpaca_camera`.`trasaction`;"
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
            database='alpaca_camera')
            action = in_action
            cursor = cnx_scope.cursor()
            query = "SELECT value, type, bash, python, get_parameter_name, get_parameter_type, get_parameter_name2, get_parameter_type2 FROM properties where name = ?"
            # print("sql query to get params is:")
            # print(query)
            # print("action value is:")
            # print(action)
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
                        # print ('trackingrate is')
                        # print(str(out_value))
                    elif type == 'dictarray':
                        out_value = ast.literal_eval(str(value_row[0][0]))
                    elif type == 'strarray':
                        out_value = ast.literal_eval(str(value_row[0][0]))
                    elif type == 'notimp':
                        out_value = 0
                        error_num = int(1024)
                        error_message = 'Gains and Offsets to be selected by a list of values in Index Mode'
                    elif type == 'imagearray':
                        #reset image ready
                        cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                        host='192.168.1.21',
                        database='alpaca_camera')
                        cursor = cnx_scope.cursor()
                        query = "UPDATE properties SET value = 'False' WHERE (name = 'imageready')"
                        cursor.execute(query)
                        cursor.close()
                        cnx_scope.commit()
                        cnx_scope.close()


                        print('trying to do stuff')
                        mimetype=request.accept_mimetypes
                        print(f"Accept Header: {mimetype}")
                        print('filename is:')
                        print(str(value_row[0][0]))
                        current_file='/opt/alpaca'+str(value_row[0][0])
                        # raw = rawpy.imread('current_file')
                        raw = rawpy.imread(str(value_row[0][0]))
                        # array = np.array(raw.raw_image)
                        array2 = np.array(raw.raw_image,dtype=np.int32)
                        #array2 = np.array(raw.postprocess(),dtype=np.int16)
                        # encoded = json.dumps(array, cls=NumpyArrayEncoder) 
                        # bytes_encoded = (array.tobytes)
                        # serialized = pickle.dumps (bytes_encoded)
                        # print (serialized)
                        # #________________________
                        # i=0
                        # j=0
                        # k=0
                        # bin_data= bytes()
                        # while i < 6064:
                        #     while j < 4040:
                        #         while k < 3:
                        #             element_in_bin= int(array2[i][j][k].astype(np.int16))
                        #             bin_data += element_in_bin.to_bytes(16,'little') 
                        #             k += 1
                        #         j += 1
                        #     i += 1

                        # #__________________________
                        # i=0
                        # j=0
                        # elemtn_100 = 100
                        # bin_data= bytes()
                        # while i < 6064:
                        #     while j < 4040:
                        #         element_in_bin= array2[i][j].item()
                        #         bin_data += element_in_bin.to_bytes(2,'little')
                        #         if elemtn_100 >0:
                        #             elemtn_100 -= 1 
                        #             print('current element int')
                        #             print(element_in_bin)
                        #             print('current element bin')
                        #             print (element_in_bin.to_bytes(2,'little'))
                        #         j += 1
                        #     i += 1
                        # print (array2)
                        # print ('Single array element:')
                        # print (array2[50][50])
                        # print (int(array2[50][50]))
                        # print (int(array2[50][50].item()))
                        print ('Array size:')                        
                        rows, columns = array2.shape
                        print(f"Array has  depth, {rows} rows, and {columns} columns.")
                        max_value = np.amax(array2)
                        print('Array maxvalue is ')
                        print(max_value)
                        print('test bynary ')
                        print(int(16383).to_bytes(2,'little'))
                        meta_version=int(1).to_bytes(4,'little')
                        meta_errorn=int(0).to_bytes(4,'little')
                        meta_ClientTransactionID=int(request.form.get('ClientTransactionID',0)).to_bytes(4,'little')
                        meta_ServerTransactionID=int(v_server_transaction).to_bytes(4,'little')
                        meta_datastart=int(44).to_bytes(4,'little')
                        meta_ImageElementType = int(2).to_bytes(4,'little')
                        meta_TransmissionElementType = int(2).to_bytes(4,'little')
                        meta_rank=int(2).to_bytes(4,'little')
                        meta_dim1= int(6064).to_bytes(4,'little')
                        meta_dim2= int(4040).to_bytes(4,'little')
                        meta_dim3= int(0).to_bytes(4,'little')



                        meta = meta_version
                        meta2 = meta + meta_errorn
                        meta3 = meta2 + meta_ClientTransactionID
                        meta4 = meta3 + meta_ServerTransactionID
                        meta5 = meta4 + meta_datastart
                        meta6 = meta5 + meta_ImageElementType
                        meta7 = meta6 + meta_TransmissionElementType
                        meta8 =  meta7 + meta_rank
                        meta9 = meta8 + meta_dim1
                        meta10 =  meta9 + meta_dim2
                        meta11 = meta10 + meta_dim3
                        little_endian_arr=np.array(array2, dtype='<i4')
                        little_endian_arr_transpose=little_endian_arr.transpose()
                        bin_data=little_endian_arr_transpose.tobytes()
                        print (meta11)
                        response_data=meta11+bin_data
                        # # out_value = encoded
                        # response_data = {response_data}
                        # headers = {'Content-Type': 'application/imagebytes'}
                        # # print (response_data)
                        # print (headers)
                        # return make_response(response_data, 200, headers)
                        response = make_response(response_data)
                        response.mimetype = 'application/imagebytes'
                        return response
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
            database='alpaca_camera')
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
            # print ('Parameter Name: '  + str(v_put_parameter_name))
            # print ('Parameter Value: '+ str(request.form.get(v_put_parameter_name)))
            # print ('Parameter Name2: '  + str(v_put_parameter_name2))
            # print ('Parameter Value2: '+ str(request.form.get(v_put_parameter_name2)))            
            #call shell for proccessing 
            if v_name=='startexposure':
                subprocess.Popen(['/bin/bash',
                                'bash_scripts_cam/put_'+v_name+'.sh', 
                                str(v_type),
                                str(v_value),
                                str(in_action), 
                                str(v_put_parameter_type),
                                str(request.form.get(v_put_parameter_name)),
                                str(request.form.get(v_put_parameter_name2)),
                                '&'
                                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.run(['/bin/bash',
                                'bash_scripts_cam/put_'+v_name+'.sh', 
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
            # print (response_data)
            # print (headers)
            return make_response(jsonify(response_data), 200, headers)
   
    else:
        # some error for not existing device!
        return 
    


if __name__ == '__main__':
    app.run(host='192.168.1.21', port=5001, debug=True)
