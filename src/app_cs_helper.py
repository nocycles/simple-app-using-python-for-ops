import class_cs_helper

while True:
    print("CS Helper.app Ver 3.0")
    print("[1] Check Electronic Application Status")
    print("[2] Blicicil Pinjam Application")
    print("[3] Motorcycle Application")
    print("[4] Check Member")
    print("[5] Check Pending Application")
    print("[6] Achievement CS")
    print("[7] Exit Program")
    pilihan = input("Select Menu: ")

    if(pilihan == '1'):
        class_cs_helper.status_pengajuan()
    elif(pilihan == '2'):
        class_cs_helper.dana_instant()
    elif(pilihan ==  '3'):
        class_cs_helper.pengajuan_motor()
    elif(pilihan ==  '4'):
        class_cs_helper.member_check()
    elif(pilihan == '5'):
        class_cs_helper.cek_pending()
    elif(pilihan == '6'):
        class_cs_helper.refcode_cs()
    elif(pilihan == '7'):
        break
    else:
        print("Invalid selection, please re-input the menu selection")
