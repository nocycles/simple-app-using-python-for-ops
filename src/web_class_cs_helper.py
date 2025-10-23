# Importing important modules
from pymongo import MongoClient
import streamlit as st
import os
import sys

filedir = os.path.dirname(os.path.abspath(__file__))
os.chdir(filedir)
os.chdir("..")
path = os.getcwd()

helper_path = os.path.join(path, "helper")
if not helper_path in sys.path:
    sys.path.append(helper_path)

from get_mongo_conn import create_parser, get_mongo_credentials, mongo_connect

os.chdir("..")
path_2 = os.getcwd()

config_path = os.path.join(path_2, "auth.conf")
parser = create_parser(config_path)

conn_string = get_mongo_credentials(parser, "mongodb_auth")
db, tbl_1, tbl_2, tbl_3, tbl_4 = ("blicicil","tbl_m_request_elektronik","tbl_m_member","tbl_m_store","tbl_m_submit_loan")
client, collection = mongo_connect(conn_string, db, tbl_1)
client, collection_2 = mongo_connect(conn_string, db, tbl_2)
client, collection_3 = mongo_connect(conn_string, db, tbl_3)
client, collection_4 = mongo_connect(conn_string, db, tbl_4)

# Streamlit UI
st.title("MongoDB Query App")

# Function to retrieve status of pengajuan
def status_pengajuan(user_input):
    if(user_input[0:2] == "08"):
        pipeline = [
            {
                '$addFields': {
                    'intStoreId': { '$toInt': '$store_id' }
                    }
            },
            {
                '$lookup': {
                    'from': 'tbl_m_member',
                    'localField': 'nik',
                    'foreignField': 'nik',
                    'as': 'joined_data'
                }
            },
            {
                '$lookup': {
                    'from': 'tbl_m_store',
                    'localField': 'intStoreId',
                    'foreignField': 'store_id',
                    'as': 'store_data'
                }
            },
            {
                '$match': {
                    'isdn': "62"+user_input[1:]
                }
            }
        ]
        document = collection.aggregate(pipeline)

    else:
        pipeline = [
            {
                '$addFields': {
                    'intStoreId': { '$toInt': '$store_id' }
                    }
            },                
            {
                '$lookup': {
                    'from': 'tbl_m_member',
                    'localField': 'nik',
                    'foreignField': 'nik',
                    'as': 'joined_data'
                }
            },
            {
                '$lookup': {
                    'from': 'tbl_m_store',
                    'localField': 'intStoreId',
                    'foreignField': 'store_id',
                    'as': 'store_data'
                }
            },
            {
                '$match': {
                    'nik': user_input
                }
            }
        ]
        document = collection.aggregate(pipeline)          
    
    # Check if the document exists
    if document:
        # Retrieve the values of the "status", "nama_pemohon", and "mobile_phone" fields
        coun = 1
        for document in document:
            status = document["status"]
            nama_pemohon = document["nama_pemohon"]
            nik = document["nik"]
            isdn = "0"+ document["isdn"][2:]
            ref_code = "Tidak ada Referral Code" if document["kode_referral"] is None else document["kode_referral"]
            try:
                latitude_user = document["lat"]
                longitude_user = document["long"]
                id_store = document["store_id"]
            except KeyError:
                latitude_user = "N/A (Pengajuan Lama)"
                longitude_user = "N/A (Pengajuan Lama)"
                id_store = "N/A (Pengajuan Lama)"                
            email = document["joined_data"][0]["email"]
            try: 
                distance = document["distance"]
            except KeyError:
                distance = "N/A (Pengajuan Lama)"
            created = document["created_at"]
            if document["store_data"]:
                store_name = document["store_data"][0]["store_name"]
                dealer_store = document["store_data"][0]["dealer_code"]
                latitude_store = str(document["store_data"][0]["latitude"])
                longitude_store = str(document["store_data"][0]["longitude"])
            else:
                store_name = "N/A (Pengajuan Lama)"
                dealer_store = "N/A (Pengajuan Lama)"
                latitude_store = "N/A (Pengajuan Lama)"
                longitude_store = "N/A (Pengajuan Lama)"
            
            # Print the results
            st.write("Data has been retrieved from the MongoDB, check the result below")
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below"))
            st.write("Data No."+ str(coun))
            st.write("Tanggal Pengajuan:", created)
            st.write("NIK              :", nik)
            st.write("Mobile Phone     :", isdn)
            st.write("Nama Pemohon     :", nama_pemohon.title())
            st.write("Status           :", status)
            st.write("Email            :", email)
            st.write("Kode Referral    :", ref_code)
            st.write("Distance (in m)  :", distance)
            st.write("Latitude User    :", latitude_user)
            st.write("Longitude User   :", longitude_user)
            st.write("Data Store / Outlet Toko")
            st.write("-"*len("Data Store / Outlet Toko"))
            st.write("Store ID         :", id_store)
            st.write("Dealer Code      :", dealer_store)
            st.write("Outlet Name      :", store_name)
            st.write("Latitude Store   :", latitude_store)
            st.write("Longitude Store  :", longitude_store)
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below"))
            st.write("")
            coun += 1
    else:
        st.write("No document found with the given 'Mobile Phone / NIK' value.")
    
    # Back to the first menu        
    st.write("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

# Function to retrieve data for Dana Instant
def dana_instant(user_input):
    type = "dana-instant"

    query = {
        "nomor_hp": user_input, "type": type
    }

    document = collection_4.find(query)
    if document:
        # Retrieve the values of the "status", "nama_pemohon", and "mobile_phone" fields
        coun = 1
        
        for document in document:
            
            status = document["status_pengajuan"]
            nama_pemohon = document["nama_konsumen"]
            nik = document["nik"]
            no_hp = document["nomor_hp"]
            no_rek = document["bank_account_no"]
            nama_rek = document["bank_account_name"]
            order_id = document["order_id"]
            order_type = document["type"]
            created = document["created_at"]
            
        # Print the results
            st.write("Data has been retrieved from the MongoDB, check the result below for Dana Instant")
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below for Dana Instant"))
            st.write("Data No."+ str(coun))
            st.write("Tanggal Pengajuan:", created)
            st.write("NIK              :", nik)
            st.write("Mobile Phone     :", no_hp)
            st.write("Nama Pemohon     :", nama_pemohon.title())
            st.write("Status           :", status)
            st.write("No Rekening      :", no_rek)
            st.write("Nama Rekening    :", nama_rek)
            st.write("Order ID         :", order_id)
            st.write("Order Type       :", order_type)
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below for Dana Instant"))
            st.write("")
            coun += 1
    else:
        st.write("No document found with the given 'Mobile Phone' value.")
    
    # Back to the first menu        
    st.write("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

# Function to retrieve data for pengajuan motor
def pengajuan_motor(user_input):
    type = "pembiayaan-motor-baru"

    query = {
        "nomor_hp": user_input, "type": type
    }

    document = collection_4.find(query)
    if document:
        # Retrieve the values of the "status", "nama_pemohon", and "mobile_phone" fields
        coun = 1
        
        for document in document:
            
            status = document["status_pengajuan"]
            nama_pemohon = document["nama_konsumen"]
            nik = document["nik"]
            no_hp = document["nomor_hp"]
            no_rek = document["bank_account_no"]
            nama_rek = document["bank_account_name"]
            order_id = document["order_id"]
            order_type = document["type"]
            created = document["created_at"]
            
        # Print the results
            st.write("Data has been retrieved from the MongoDB, check the result below for Dana Instant")
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below for Dana Instant"))
            st.write("Data No."+ str(coun))
            st.write("Tanggal Pengajuan:", created)
            st.write("NIK              :", nik)
            st.write("Mobile Phone     :", no_hp)
            st.write("Nama Pemohon     :", nama_pemohon.title())
            st.write("Status           :", status)
            st.write("No Rekening      :", no_rek)
            st.write("Nama Rekening    :", nama_rek)
            st.write("Order ID         :", order_id)
            st.write("Order Type       :", order_type)
            st.write("="*len("Data has been retrieved from the MongoDB, check the result below for Dana Instant"))
            st.write("")
            coun += 1
    else:
        st.write("No document found with the given 'Mobile Phone' value.")
    
    # Back to the first menu        
    st.write("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

def member_check():
    st.write("Soon to be updated on the next version!")
    st.write("Press Any Key To Back into First Menu")
    input()
    os.system('cls')    

def cek_pending(date_input_1,date_input_2):
    
    start_date = date_input_1
    end_date = date_input_2
    
    query_filter = {
        'created_at': {
            '$gte' : start_date,
            '$lte' : end_date
        },
        'status':'PENDING'
    }

    document_count = collection.count_documents(query_filter)
    document = collection.find(query_filter)
    
    time = document["created_at"][0]
    st.write(f"")
    st.write(f"Total documents with status PENDING between {start_date} and {end_date}: {document_count}")
    st.write("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

# Main function
def main():
    menu = st.sidebar.selectbox("Menu", ["Status Pengajuan", "Dana Instant", "Pengajuan Motor", "Member Check", "Cek Pending"])

    if menu == "Status Pengajuan":
        st.subheader("Status Pengajuan")
        user_input = st.text_input("Input Mobile Phone / NIK:")
        if st.button("Submit"):
            status_pengajuan(user_input)
    elif menu == "Dana Instant":
        st.subheader("Dana Instant")
        user_input = st.text_input("Input Mobile Phone:")
        if st.button("Submit"):
            dana_instant(user_input)
    elif menu == "Pengajuan Motor":
        st.subheader("Pengajuan Motor")
        user_input = st.text_input("Input Mobile Phone:")
        if st.button("Submit"):
            pengajuan_motor(user_input)
    elif menu == "Member Check":
        st.subheader("Member Check")
        member_check()
    elif menu == "Cek Pending":
        st.subheader("Cek Pending")
        date_input_1 = st.text_input("Input Start Date  : ")
        date_input_2 = st.text_input("Input End Date    : ")
        cek_pending(date_input_1,date_input_2)

if __name__ == "__main__":
    main()
