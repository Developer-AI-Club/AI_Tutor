"nhap giu lieu vao"
matkhau = input("Hay nhap vao 1 may khau :")
"kiem tra mk"
result= False

if len(matkhau)>=6:
    if len(matkhau)<=12:
        if matkhau.isupper() == False:
            if matkhau.islower() == False:
                if matkhau.isdecimal() == True:
                    for i in matkhau:

                        if i.isdecimal() == True:

                         result = True
if result==False:
    print("Mat khau khong hop le ")
else :
    print("Mat khau hop le")