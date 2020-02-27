def get_binary(variables,mintermss):
    list1={}

    for i in range (len(mintermss)):
        if(int(mintermss[i])>=pow(2,variables)):
            continue
        if len(bin(int(mintermss[i]))[2:].zfill(variables))>variables:
            print("minterm "+mintermss[i]+"diluar batas bit")
            continue
        list1.update({int(mintermss[i]):bin(int(mintermss[i]))[2:].zfill(variables)})
        mintermss[i]=bin(int(mintermss[i]))[2:].zfill(variables)
    print ("{:<8} {:<15} ".format('minterms','binary'))
    for k, v in list1.items():
        binary= v
        print ("{:<8} {:<15}".format(k, binary))
    return mintermss,list1

def grouping_minterms(masuk,jumlah):
    
    minterms_categorised={}
    show_minterms={}
    for i in range(jumlah+1):
         minterms_categorised[i]=[]
    
    for i in range(jumlah+1): #kekurangan 1 dari looping adalah menghasilkan dictionary dengan value []
        for x in masuk:
            if (x.count("1")==i):
                    minterms_categorised[i].append([x,[int(x,2)]]) #mengubah x menjadi bilangan decimalnya
    show_minterms.update(minterms_categorised)
    for i in range(jumlah+1):
        if(minterms_categorised[i]==[]):
            del minterms_categorised[i] 
        
    return minterms_categorised,show_minterms

def check(minterms1,minterms2):
    count=0
    combined=[]  
    for i in range (len(minterms1[0])):
        combined.append(minterms1[0][i])
        if minterms2[0][i]!=minterms1[0][i]:
            combined[i]='-'
            count+=1 
    if count>1:
        return 0
    else:
        return ["".join(combined),minterms1[1]+minterms2[1]]

def flatten(x): #  convert dictionary into a list
    removed_groups = []
    for i in x:
        removed_groups.extend(x[i]) 
    return removed_groups

def get_prime_implicant(group,variable,prime_implicant,no):
    combine=[]
    centang=[]
    recrusion=0
    new_minterms={}
    if no>1:
        list1=flatten(group)
        print("")
        print("ini loop ke-",no)
        print ("{:<15} {:<15} ".format('minterms','binary'))
        for i in range(len(list1)):
            y=list1[i][0]
            x=str(list1[i][1])[1:-1]
            print ("{:<15} {:<15}".format(x, y))   

    flag=0
    for i in range(variable):
        new_minterms[i]=[]
    for i in range(variable): #flag tidak direset atau dibuat == 0 kembali karena memungkinkan list m bukan prime implicant                    
        for m in group[i]:      # ter-apend ke list prime implicant karena kemungkinan antara list m dan list n tidak
            for n in group[i+1]: #ada yang memiliki kemiripan
                combine=check(m,n)
                if combine !=0:
                    flag=1 
                    recrusion=1
                    new_minterms[i].append(combine)
                    if m not in centang:
                        centang.append(m)
                    if n not in centang:
                        centang.append(n)
            if flag==0 and  m not in centang and n not in [x[0] for x in prime_implicant]:
                prime_implicant.append(m)

    for i in group[variable]:
         if i not in centang and i[0] not in [x[0] for x in prime_implicant]:
            prime_implicant.append(i)
            #loop khusus karena pada dictionary dengan key sama dengan jumlah maksimum bit 1 pada setiap 
            #kali pemanggilan fungsi rekrusif. Karena diakibatkan loop sebelumnya ada kemungkinan bahwa 
            #indeks/key terakhir tersebut merupakan prime implicant tetapi tidak ter append karena flag=1(alasan di comment sebelumnya)
    if recrusion==0:
        return prime_implicant
    else:
        get_prime_implicant(new_minterms,variable-1,prime_implicant,no+1)
        
def main():
    print("choose sum of variabble = ",end=" ")
    n=int(input())
    method_s=input("Pilih Metode [pos/sop] : ")
    print("variabel : ",end=" ")
    variable=list(input().split(",",maxsplit=n)[:n])
    print("allow don't care?[y/n")
    dc_allow=input()
    dc=[]
    if method_s=="sop" or method_s=="SOP":
        print("Input Minterms = ",end=" ")
        minterms=list(input().split(",",maxsplit=pow(2,n)))
        if dc_allow=='y'or dc_allow=='Y':
            print("input DC : ",end=" ")
            dc=list(input().split(',',maxsplit=16-len(minterms)))
            minterms=minterms+dc
    elif method_s=="pos" or method_s=="POS":
        print("Input maxterm = ",end=" ")
        minterms=list(input().split(",",maxsplit=pow(2,n)))
        if dc_allow=='y'or dc_allow=='Y':
            print("input DC : ",end=" ")
            dc=list(input().split(',',maxsplit=16-len(minterms)))
            minterms=minterms+dc

    print("f",end="") 
    print(([variable[i] for i in range(n)] ),end="") 
    print( " \u03A3 m = ",minterms )
    minterms,dic_minterms=get_binary(n,minterms)
    print(minterms)
    minterms_group={}
    show_minterms={}
    minterms_group,show_minterms=grouping_minterms(minterms,n)
    print("")
    print("")
    print("hasil  loop ke -1:")
    list1=flatten(minterms_group)#flatten dict lalu 
    #show dictionary tanpa menampilkan key dengan value []
    print ("{:<15} {:<15}".format("minterms", "binary"))
    for i in range(len(list1)):
            y=list1[i][0]
            x=str(list1[i][1])[1:-1]
            print ("{:<15} {:<15}".format(x, y))
    prime_implicant=[]
    prime_implicant.append(get_prime_implicant(show_minterms,n,prime_implicant,1)) 
    #parameter yang digunakan adalah dictionary hasil grouping satu yang memiliki value [] 
    # agar tidak terjadi error saat membandingkan ("out of index")
    prime_implicant.remove(None)
    print("")
    print("")
    print("prime implicant chart : ")
    print("")
    tampil=''.join(variable)
    print ("{:<15} {:<15}".format("",str(tampil)))
    tampil=[]
    for i in range(len(prime_implicant)):
         x=str(prime_implicant[i][1])[1:-1]
         y=prime_implicant[i][0]
         print ("{:<15} {:<15}".format(x,y))
    print("")
    fungsi=[]
 

if __name__ == '__main__':
    main()