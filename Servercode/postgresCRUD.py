import psycopg2
import datetime
import logging
from datetime import timedelta

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
        
        logging.basicConfig(level=logging.INFO, filename='mr_motion_db_insert.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.info("mr motion data inserted successfully at " + str(datetime.datetime.now()))
        
    except (Exception, psycopg2.Error) as error:
        logging.basicConfig(level=logging.DEBUG, filename='mr_motion_err.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.error("Error inserting mr tof data at "  + str(datetime.datetime.now()))
            
    finally:
        if (conn):
            cursor.close()
            connection.close()
            
def insert_tof_details(mr_id,mr_ts,mr_count):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        retrieve_query = """SELECT * from mr_count_hist where meetingroomid= %s DESC LIMIT 1"""      
        cursor.execute(retrieve_query,(mr_id,))
        count_record = cursor.fetchall()
        for count in count_records:
            mr_count += count[2]
        
        insert_query = """ INSERT INTO mr_count_hist(meetingroomid,mrcounttimestamp,count) VALUES (%s,%s,%s)"""
        
        to_insert = (mr_id,mr_ts,mr_count)
        
        cursor.execute(insert_query,to_insert)
        conn.commit()
        
        logging.basicConfig(level=logging.INFO, filename='mr_tof_db_insert.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.info("mr tof data inserted successfully at "  + str(datetime.datetime.now()))
        
    except (Exception, psycopg2.Error) as error:
        logging.basicConfig(level=logging.DEBUG, filename='mr_tof_err.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.error("Error inserting mr tof data at " + str(datetime.datetime.now()))
            
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
        
        logging.basicConfig(level=logging.INFO, filename='hd_db_insert.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.info("hd data inserted successfully into the database at "  + str(datetime.datetime.now()))
        
    except (Exception, psycopg2.Error) as error:
        logging.basicConfig(level=logging.DEBUG, filename='hd_err.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.error("Error inserting hd data at "  + str(datetime.datetime.now()))
            
    finally:
        if (conn):
            cursor.close()
            connection.close()

def update_hd_hb(t_id, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        update_query = """
        UPDATE heartbeat SET timestamp = (%s) WHERE id = (%s)
        """

        to_insert = (timestamp, t_id)

        cursor.execute(update_query,to_insert)
        conn.commit()
        
        logging.basicConfig(level=logging.INFO, filename='hb_db_insert.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.info("hb data inserted successfully into the database at " + str(datetime.datetime.now()))
        
    except (Exception, psycopg2.Error) as error:
        logging.basicConfig(level=logging.DEBUG, filename='hb_err.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.error("Error inserting hb data at " + str(datetime.datetime.now()))
            
    finally:
        if (conn):
            cursor.close()
            connection.close()        
            
def update_motion_hc(status):
    timestamp = str(datetime.datetime.now() + timedelta(hours=8))
    
    logging.basicConfig(level=logging.INFO, filename='motion_hc_insert.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.info(status + timstamp)
             