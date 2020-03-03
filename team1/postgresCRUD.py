import psycopg2
import datetime

def get_connection():
    return psycopg2.connect(user="mqttuser", password="iott1t5", host="127.0.0.1", port="5432", database="R77_OCCUPANCY")
    
def insert_motion_details(hd_id,hd_ts,hd_status): # change the parameter 
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        insert_query = """ INSERT INTO hd_occ_hist(hotdeskid,hdocctimestamp,occstatus) VALUES (%s,%s,%s)""" # change the insert statement
        
        to_insert = (hd_id,hd_ts,hd_status) # change this to the same as parameter
        
        cursor.execute(insert_query,to_insert)
        conn.commit()
        
        f = open("successful.txt","a")
        f.write("Successful inserting hd occ status @ " + str(datetime.datetime.now()))
        f.close()
        
    except (Exception, psycopg2.Error) as error:
        print(str(error))
        f = open("error.txt","a")
        f.write("Error inserting hd occ status @ " + str(datetime.datetime.now()))
        f.close()
            
    finally:
        if (conn):
            cursor.close()
            connection.close()