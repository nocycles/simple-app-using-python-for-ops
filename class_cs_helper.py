#Importing important module
from pymongo import MongoClient
import pymongo
import os
from tabulate import tabulate

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
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return status_pengajuan()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value")

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
            similarity = document["name_similarity"]
            
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
            print("Name Similarity  :", similarity)
            print("="*len(msg))
            print("")
            coun = coun + 1
    else:
        print("No document found with the given 'Mobile Phone' value.")
    
    #Back to the first menu        
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return dana_instant()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value")

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
            similarity = document["name_similarity"]
            
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
            print("Name Similarity  :", similarity)
            print("="*len(msg))
            print("")
            coun = coun + 1
    else:
        print("No document found with the given 'Mobile Phone' value.")
    
    #Back to the first menu        
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return pengajuan_motor()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value")

def member_check():
    msg = "Please refer to this format of phone number 08xxxx"
    print(msg)
    print("-"*len(msg))
    user_input = input("Input Mobile Phone: ")

    pipeline = [               
            {
                '$lookup': {
                    'from': 'tbl_device_info',
                    'localField': 'deviceid',
                    'foreignField': 'device_id',
                    'as': 'joined_data'
                }
            },
            {
                '$match': {
                    'mobile_phone': user_input[1:]
                }
            }
        ]
    
    documents = collection_2.aggregate(pipeline)

    if documents:
        for document in documents:
            created_at = document["created_at"]
            try:
                ktp_date = document["ktp_verify_date"]
            except KeyError:
                ktp_date = "Belum Melakukan Proses Verifikasi KTP"
            name = document["name"]
            email = document["email"]
            mobile_phone = document["mobile_phone"]
            try:
                nik = document["nik"]
            except KeyError:
                nik = "N/A Belum Proses Verifikasi KTP"
            #try:
            #    device_model = document["joined_data"][0]["device_desc"]
            #except KeyError:
            #    device_model = "N/A Tidak diketahui jenis device"    
            try: 
                re_verified = str(document["is_re_verified"])
            except KeyError:
                re_verified = "True"
            if re_verified == "True":
                result_re_verified = "Sudah Melakukan Verifikasi Ulang"
            else:
                result_re_verified = "Belum Melakukan Verifikasi Ulang"
            code = str(document["code"])
            if code == "None":
                result_code = "Sudah Input Kode OTP"
            else:
                result_code = "Belum Input Kode OTP"
            
            print("-"*len(msg))
            print("Nama User                :", name.title())
            print("No. Handphone            :", mobile_phone)
            print("Email                    :", email.lower())
            print("Tanggal Regist           :", created_at)
            print("NIK                      :", nik)
            print("Tanggal Verifikasi KTP   :", ktp_date)
            print("Status Verifikasi Ulang  :", result_re_verified)
            print("Status OTP               :", result_code)
            #print("Model Handphone          :", device_model)
    else:
        print("No accounts have been found from the Mobile Phone given")

    #Back to the first menu    
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return member_check()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value") 

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
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return cek_pending()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value")

def refcode_cs():
    msg = "Select profile in here"
    print(msg)
    print("-"*len(msg))
    msg_rizky = "[1] Rizky Indah"
    msg_yuni = "[2] Jessica"
    msg_lidya = "[3] Angel"
    print(msg_rizky)
    print(msg_yuni)
    print(msg_lidya)
    print("-"*len(msg_lidya))
    user = str(input("Select between 1, 2, and 3: "))
    cs_1 = "^rzk"
    cs_2 = "^jsc"
    cs_3 = "^agl"
    if user == "1":
        query = {
            'kode_referral': {
                '$regex': cs_1,
                '$options': 'i'
            }
        }
        documents_1 = collection.find(query).sort([("created_at",pymongo.DESCENDING)])

        # Extract and format specific fields from the documents for distinct 'nik' values
        formatted_documents = []
        for document in documents_1:
            formatted_document = [document.get("created_at", ""), 
                                    document.get("nik", ""),
                                    document.get("nama_pemohon", "").title(), 
                                    document.get("kode_referral", "").upper(),                               
                                    document.get("isdn", "")[2:],
                                    document.get("kote").title(),
                                    document.get("alamat_domisili")
                                    ]
            formatted_documents.append(formatted_document)

        # Check if any documents were found
        if not formatted_documents:
            print("No documents found.")
        else:
            # Flag the first few documents
            flagged_documents = formatted_documents
            
            # Display the flagged documents in a table
            headers = ["Date", "NIK", "Nama Konsumen", "Kode_Referral", "Phone Number","Kota", "Alamat Domisili" ]
            print(tabulate(flagged_documents, headers=headers, tablefmt="simple"))

        # Display the count of distinct 'nik' values found
        count = len(formatted_documents)
        print(f"Total applications found by Referral Code: {count}")

    elif user == "2":
        query = {
            'kode_referral': {
                '$regex': cs_2,
                '$options': 'i'
            }
        }
        documents_2 = collection.find(query).sort([("created_at",pymongo.DESCENDING)])

        # Extract and format specific fields from the documents for distinct 'nik' values
        formatted_documents = []
        for document in documents_2:
            formatted_document = [document.get("created_at", ""), 
                                    document.get("nik", ""),
                                    document.get("nama_pemohon", "").title(), 
                                    document.get("kode_referral", "").upper(),                               
                                    document.get("isdn", "")[2:],
                                    document.get("kote").title(),
                                    document.get("alamat_domisili")
                                    ]
            formatted_documents.append(formatted_document)

        # Check if any documents were found
        if not formatted_documents:
            print("No documents found.")
        else:
            # Flag the first few documents
            flagged_documents = formatted_documents
            
            # Display the flagged documents in a table
            headers = ["Date", "NIK", "Nama Konsumen", "Kode_Referral", "Phone Number","Kota", "Alamat Domisili" ]
            print(tabulate(flagged_documents, headers=headers, tablefmt="simple"))

        # Display the count of distinct 'nik' values found
        count = len(formatted_documents)
        print(f"Total applications found by Referral Code: {count}")

    elif user == "3":
        query = {
            'kode_referral': {
                '$regex': cs_3,
                '$options': 'i'
            }
        }
        documents_3 = collection.find(query).sort([("created_at",pymongo.DESCENDING)])

        # Extract and format specific fields from the documents for distinct 'nik' values
        formatted_documents = []
        for document in documents_3:
            formatted_document = [document.get("created_at", ""), 
                                    document.get("nik", ""),
                                    document.get("nama_pemohon", "").title(), 
                                    document.get("kode_referral", "").upper(),                               
                                    document.get("isdn", "")[2:],
                                    document.get("kote").title(),
                                    document.get("alamat_domisili")
                                    ]
            formatted_documents.append(formatted_document)

        # Check if any documents were found
        if not formatted_documents:
            print("No documents found.")
        else:
            # Flag the first few documents
            flagged_documents = formatted_documents
            
            # Display the flagged documents in a table
            headers = ["Date", "NIK", "Nama Konsumen", "Kode_Referral", "Phone Number","Kota", "Alamat Domisili" ]
            print(tabulate(flagged_documents, headers=headers, tablefmt="simple"))

        # Display the count of distinct 'nik' values found
        count = len(formatted_documents)
        print(f"Total applications found by Referral Code: {count}")
    else:
        "Didn't match the required value"
        return refcode_cs()
    while True:
        confirmation = input("\nDo you want to stay in this menu or back to first menu? <y/n>: ")
        if confirmation == "Y" or confirmation == "y":
            return refcode_cs()
        elif confirmation == "N" or confirmation == "n":
            os.system('cls')
            break
        else:
            print("Didn't match the required value")