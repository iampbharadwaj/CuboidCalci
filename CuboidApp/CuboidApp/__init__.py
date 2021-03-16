from flask import Flask, jsonify, request
import pymysql
import time
import datetime
# from flaskext.mysql import MySQL

# from flask.ext.mysql import MySQL


app = Flask(__name__)

# Creating a connection cursor
db_connection = pymysql.connect(host='85.215.232.156',
        user='test_user',
        password='test_pwd',
        db='cuboid_result_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

cursor = db_connection.cursor()

def find_surface_area(side_length, side_height, side_width):
    return 2 * ((side_length * side_height) + (side_height * side_width) + (side_width * side_length))

def find_volume(side_length, side_height, side_width):
    return side_length * side_height * side_width


def find_sum_of_edges(side_length, side_height, side_width):
    return 4 * (side_length + side_height + side_width)


@app.route('/')
def hello():
    return 'Welcome to the Cuboid Calculator Page'



@app.route('/cuboid/calculate', methods=['POST'])
def cuboid_calcuate():
    data = request.get_json()
    types_of_edge_list = []
    values_of_edge_list = []
    edges = data['cuboid_edges']
    if len(edges) != 3:
        status_code = 400
        success = False
        error = f'Requires exactly 3 parameters'
        response = {'success': success, 'error': error}
        print('response=',jsonify(response))
        return jsonify(response), status_code
    else:
        for value in edges:
            if isinstance(value, (float, int)):
                types_of_edge_list.append(True)
            else:
                types_of_edge_list.append(False)
        if all(types_of_edge_list) is False:
            status_code = 400
            success = False
            error = f'Invalid type of Input given, Provide either float or int values for cuboid edges'
            response = {'success': success, 'error': error}
            return jsonify(response), status_code
        else:
            for value in edges:
                if value <= 0:
                    values_of_edge_list.append(False)
                else:
                    values_of_edge_list.append(True)
            if all(values_of_edge_list) is False:
                status_code = 400
                success = False
                error = f'Found one of the cuboid edges <= 0, please provide all the edges > 0'
                response = {'success': success, 'error': error}
                return jsonify(response), status_code
            else:
                edges = [float(val) for val in edges]
                length, height, width = edges
                surface_area = find_surface_area(length, height, width)
                volume = find_volume(length, height, width)
                sum_of_edges = find_sum_of_edges(length, height, width)
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                # Write the result into DB
                try:
                    db_connection = pymysql.connect(host='85.215.232.156', user='test_user', password='test_pwd', 
                            db='cuboid_result_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
                    cursor = db_connection.cursor()
                    mysql_insert_query= ''' INSERT INTO cuboid_result_table (timestamp, length, height, width, surface_area, volume, sum_of_edges) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                    record=(timestamp, length, height, width, surface_area, volume, sum_of_edges)
                    cursor.execute(mysql_insert_query, record)
                    db_connection.commit()
                    status_code = 200
                    success = True
                    error = None
                    data = {'surface_area': surface_area, 'volume': volume, 'sum_of_edges': sum_of_edges}
                    response = {'success': success, 'data': data, 'error': error}
                except (IndexError, TypeError, ValueError) as e:
                    db_connection.rollback()
                    status_code = 500
                    success = False
                    error = e
                    response = {'success': success, 'error': error}
                finally:
                    cursor.close()
                    db_connection.close()
                    return jsonify(response), status_code


@app.route('/cuboid/result', methods=['GET'])
def cuboid_get_all_results():
    # Get the results from the DB
    try:
        db_connection = pymysql.connect(host='85.215.232.156', user='test_user', password='test_pwd',
                db='cuboid_result_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = db_connection.cursor()
        cursor.execute(''' SELECT * FROM cuboid_result_table''')
        result = list(cursor.fetchall())
        status_code = 200
        success = True
        error = None
        data = result
        response = {'success': success, 'data': data, 'error': error}
    except Exception as e:
        status_code = 500
        success = False
        error = e
        response = {'success': success, 'error': error}
    finally:
        cursor.close()
        db_connection.close()
        return jsonify(response), status_code


@app.route('/cuboid/result/<number>', methods=['GET'])
def cuboid_get_number_of_results(number):
    try:
        db_connection = pymysql.connect(host='85.215.232.156', user='test_user', password='test_pwd',
                db='cuboid_result_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = db_connection.cursor() 
        # Get the n number for rows from the DB
        cursor.execute(f''' SELECT * FROM cuboid_result_table ORDER BY id DESC LIMIT {number}''')
        result = list(cursor.fetchall())
        status_code = 200
        success = True
        error = None
        data = result
        response = {'success': success, 'data': data, 'error': error}
    except Exception as e:
        status_code = 500
        success = False
        error = e
        response = {'success': success, 'error': error}
    finally:
        cursor.close()
        db_connection.close()
        return jsonify(response), status_code



if __name__ == "__main__":
    app.run()
