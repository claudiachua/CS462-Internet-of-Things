import psycopg2
import datetime

def get_connection():
    return psycopg2.connect(user="mqttuser", password="iott1t5", host="127.0.0.1", port="5432", database="R77_OCCUPANCY")
    
def insert_motion_details(mr_id,mr_ts,mr_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        insert_query = """ INSERT INTO mr_occ_hist(meetingroomid,mrocctimestamp,occstatus) VALUES (%s,%s,%s)"""
        
        to_insert = (mr_id,mr_ts,mr_status)
        
        cursor.execute(insert_query,to_insert)
        conn.commit()
        
        f = open("successful.txt","a")
        f.write("\n Successful inserting mr occ status @ " + str(datetime.datetime.now()))
        f.close()
        
    except (Exception, psycopg2.Error) as error:
        print(str(error))
        f = open("error.txt","a")
        f.write("\n Error inserting mr occ status @ " + str(datetime.datetime.now()))
        f.close()
            
    finally:
        if (conn):
            cursor.close()
            connection.close()
            
def insert_tof_details(mr_id,mr_ts,mr_count):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        insert_query = """ INSERT INTO mr_count_hist(meetingroomid,mrcounttimestamp,count) VALUES (%s,%s,%s)"""
        
        to_insert = (mr_id,mr_ts,mr_count)
        
        cursor.execute(insert_query,to_insert)
        conn.commit()
        
        f = open("successful.txt","a")
        f.write("\n Successful inserting mr occ count @ " + str(datetime.datetime.now()))
        f.close()
        
    except (Exception, psycopg2.Error) as error:
        print(str(error))
        f = open("error.txt","a")
        f.write("\n Error inserting mr occ count @ " + str(datetime.datetime.now()))
        f.close()
            
    finally:
        if (conn):
            cursor.close()
            connection.close()

def insert_hd_details(hd_id,hd_ts,hd_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        insert_query = """ INSERT INTO hd_occ_hist(hotdeskid,hdocctimestamp,occstatus) VALUES (%s,%s,%s)"""
        
        to_insert = (hd_id,hd_ts,hd_status)
        
        cursor.execute(insert_query,to_insert)
        conn.commit()
        
        f = open("successful.txt","a")
        f.write("\n Successful inserting hd occ status @ " + str(datetime.datetime.now()))
        f.close()
        
    except (Exception, psycopg2.Error) as error:
        print(str(error))
        f = open("error.txt","a")
        f.write("\n Error inserting hotdesk occ status @ " + str(datetime.datetime.now()))
        f.close()
            
    finally:
        if (conn):
            cursor.close()
            connection.close()