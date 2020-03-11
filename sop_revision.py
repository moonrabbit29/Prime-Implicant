def bitcomparing(minterms1,minterms2):
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
def get_primeimplicant(minterms,primeimplicant,maximumbit,count): #combine list
    checklist=[]
    new_minterms={}
    recrusion=0
    if count>1:
        list1=flatten(minterms)
        print("\n ini loop ke-",count)
        print ("{:<15} {:<15} ".format('minterms','binary'))
        for i in range(len(list1)):
            y=list1[i][0]
            x=str(list1[i][1])[1:-1]
            print ("{:<15} {:<15}".format(x, y))
    for i in range(maximumbit):
        new_minterms[i]=[]
        for m in minterms[i]:
            for n in minterms[i+1]:
                combime=bitcomparing(m,n)
                if combime!=0:
                    new_minterms[i].append(combime)
                    if m not in checklist:
                        checklist.append(m)
                    if n not in checklist:
                        checklist.append(n)
                    recrusion=1
            if m not in checklist and m[0] not in [x[0] for x in primeimplicant]:
                primeimplicant.append(m)
    for x in minterms[maximumbit]:
        if x not in checklist and x[0] not in [x[0] for x in primeimplicant]:
            primeimplicant.append(x)
    if recrusion==0:
        return primeimplicant
    elif recrusion==1:
        get_primeimplicant(new_minterms,primeimplicant,maximumbit-1,count+1)

    

if __name__ == '__main__':
    n=int(input("Masukan jumlah maksimum bit : "))
    variable=list(input("Masukan Variable sejumlah maximum bit: ").split(maxsplit=4))
    print(variable)
    minterms=list(int(i) for i in (input("Masukan minterms: ").strip().split()) if int(i) <pow(2,n))
    dc=list(int(i) for i in (input("Masukan dc, enter apabila tidak ada don't care : ").strip().split()) if int(i) not in minterms and int(i)<pow(2,n))
    method=input("Masukan metode SOP/POS : ") 
    if(method=="SOP"):
        mt=minterms+dc
    elif(method=="POS"):
        temp=minterms+dc
        mt=[i for i in range(pow(2,n)) if i not in temp]
        mt=mt+dc
    for i in range(len(mt)):
        mt[i]=bin(mt[i])[2:].zfill(n)
    minterms_categorised={}
    for i in range(n+1):
         minterms_categorised[i]=[]
    for x in mt: 
        minterms_categorised[x.count("1")].append([x,[int(x,2)]])
    primeimplicant=[]
    primeimplicant.append(get_primeimplicant(minterms_categorised,primeimplicant,n,0))
    primeimplicant.remove(None)
    tampil=''.join(variable)
    print("\n \n prime inplicant chart:")
    print ("\n \n {:<15} {:<15}".format("",str(tampil)))
    for i in range(len(primeimplicant)):
         x=str(primeimplicant[i][1])[1:-1]
         y=primeimplicant[i][0]
         print ("{:<15} {:<15}".format(x,y))
    

    
    

