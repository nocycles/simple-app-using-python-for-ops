import class_cs_helper

while True:
    print("CS Helper.app Ver 2.1")
    print("[1] Status Pengajuan ")
    print("[2] Dana Instant")
    print("[3] Pengajuan Motor")
    print("[4] Member")
    print("[5] Cek Pending Slik")
    print("[6] Exit Program")
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
        break
    else:
        print("Invalid selection, please re-input the menu selection")
