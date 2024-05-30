#Importing important module
from pymongo import MongoClient
import os

#Connection to Database
file = open("D:\Raymond\Raymond's Work\python_trial\code_python\pass_mongo.txt",'r')
client = MongoClient(f"mongodb://{file.readline()}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client.blicicil
collection = db.tbl_m_request_elektronik
collection_2 = db.tbl_m_member
collection_3 = db.tbl_m_store
collection_4 = db.tbl_m_submit_loan


def status_pengajuan() :
    user_input = input("Input Mobile Phone / NIK: ")

    # Search for the document with the matching "nik" value   
    if(user_input[0:2] == "08") : 
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
            if document["kode_referral"]== None:
                ref_code = "Tidak ada Referral Code"
            else:
                ref_code = document["kode_referral"]
            try:
                latitude_user = document["lat"]
                longitude_user = document["long"]
                id_store = document["store_id"]
            except KeyError:
                latitude_user = "N/A (Pengajuan Lama)"
                longitude_user = "N/A (Pengajuan Lama)"
                id_store = "N/A (Pengajuan Lama)"                
            #for tbl_member in document["joined_data"][0]:
            #    email = email + tbl_member["email"] +  "/" 
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
            msg=("Data has been retrieved from the MongoDB, check the result below")
            print(msg)
            print("="*len(msg))
            print("Data No."+ str(coun))
            print("Tanggal Pengajuan:", created)
            print("NIK              :", nik)
            print("Mobile Phone     :", isdn)
            print("Nama Pemohon     :", nama_pemohon.title())
            print("Status           :", status)
            print("Email            :", email)
            print("Kode Referral    :", ref_code)
            print("Distance (in m)  :", distance)
            print("Latitude User    :", latitude_user)
            print("Longitude User   :", longitude_user)
            msg2 = ("Data Store / Outlet Toko")
            print("-"*len(msg2))
            print(msg2)              
            print("Store ID         :", id_store)
            print("Dealer Code      :", dealer_store)
            print("Outlet Name      :", store_name)
            print("Latitude Store   :", latitude_store)
            print("Longitude Store  :", longitude_store)
            print("="*len(msg))
            print("")
            coun = coun + 1
    else:
        print("No document found with the given 'Mobile Phone / NIK' value.")
    
    #Back to the first menu        
    print("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

def dana_instant():
    user_input = input("Input Mobile Phone: ")
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
            msg=("Data has been retrieved from the MongoDB, check the result below for Dana Instant")
            print(msg)
            print("="*len(msg))
            print("Data No."+ str(coun))
            print("Tanggal Pengajuan:", created)
            print("NIK              :", nik)
            print("Mobile Phone     :", no_hp)
            print("Nama Pemohon     :", nama_pemohon.title())
            print("Status           :", status)
            print("No Rekening      :", no_rek)
            print("Nama Rekening    :", nama_rek)
            print("Order ID         :", order_id)
            print("Order Type       :", order_type)
            print("="*len(msg))
            print("")
            coun = coun + 1
    else:
        print("No document found with the given 'Mobile Phone' value.")
    
    #Back to the first menu        
    print("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

def pengajuan_motor():
    user_input = input("Input Mobile Phone: ")
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
            msg=("Data has been retrieved from the MongoDB, check the result below for Dana Instant")
            print(msg)
            print("="*len(msg))
            print("Data No."+ str(coun))
            print("Tanggal Pengajuan:", created)
            print("NIK              :", nik)
            print("Mobile Phone     :", no_hp)
            print("Nama Pemohon     :", nama_pemohon.title())
            print("Status           :", status)
            print("No Rekening      :", no_rek)
            print("Nama Rekening    :", nama_rek)
            print("Order ID         :", order_id)
            print("Order Type       :", order_type)
            print("="*len(msg))
            print("")
            coun = coun + 1
    else:
        print("No document found with the given 'Mobile Phone' value.")
    
    #Back to the first menu        
    print("Press Any Key To Back into First Menu")
    input()
    os.system('cls')

def member_check():
    print("Soon to be updated on the next version!")
    print("Press Any Key To Back into First Menu")
    input()
    os.system('cls')    

def cek_pending():
    
    start_date = input("Enter the start date (example: 2023-06-01): ")
    end_date = input("Enter the end date (example: 2023-06-02): ")
    
    query_filter = {
        'created_at': {
            '$gte' : start_date,
            '$lte' : end_date
        },
        'status':'PENDING'
    }

    document_count = collection.count_documents(query_filter)
    documents = collection.find(query_filter)
    
    if document_count > 0:
        if documents:
            document=[]
            for docs in documents:
                created_at = docs["created_at"]
                document.append(created_at)
        else:
            print("No document found with the given 'Mobile Phone' value.")
        time = document[0][11:]
        msg1 = f"\nFirst pending at: {time} WIB"
        msg2 = f"Total documents with status PENDING between {start_date} and {end_date}: {document_count}"
        print("-"*25)
        print(msg1)
        print(msg2)
        
    msg3 = "There are no pending case at your desired date"
    print("-"*len(msg3))
    print(msg3)
    print("\nPress Any Key To Back into First Menu")
    input()
    os.system('cls')