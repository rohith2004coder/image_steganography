from PIL import Image
from Crypto.Cipher import AES

############################################
############################################
def encode_img(new_img,data):
    x,y=0,0
    lendata=len(data)
    imdata=iter(new_img.getdata())
    for i in range(lendata):
        s=format(data[i],"08b")
        #print(s)##############################
        l=list(imdata.__next__())+list(imdata.__next__())+list(imdata.__next__())
        for j in range(8):
            if (s[j]=='0' and l[j]&1):
                l[j]-=1
            elif (s[j]=='1' and not(l[j]&1)):
                l[j]+=1
        if (i+1!=lendata and not(l[8]&1)):
            l[8]+=1
        elif (i+1==lendata and l[8]&1):
            l[8]-=1
        pix1=tuple(l[0:3]+[255,])
        pix2=tuple(l[3:6]+[255,])
        pix3=tuple(l[6:]+[255,])
        new_img.putpixel((x,y),pix1)
        x+=1
        new_img.putpixel((x,y),pix2)
        x+=1
        new_img.putpixel((x,y),pix3)
        x+=1

############################################

def decode_img(new_img):
    x,y=0,0
    int_arr=[]
    imdata=iter(new_img.getdata())
    cipher_int_form=[]
    while(True):
        l=list(imdata.__next__())+list(imdata.__next__())+list(imdata.__next__())
        x=0
        '''bit*2+1'''
        for i in range(8):
            if (l[i]&1):
                x=x*2+1
            else:
                x=x*2
        cipher_int_form.append(x)
        if (not(l[-1]&1)):
            break
    #return cipher_int_form
    cipher_bytes_list = [x.to_bytes(1,'little') for x in cipher_int_form]
    cipher_bytes = b''.join(i for i in cipher_bytes_list)
    return cipher_bytes


#hv=0#############################------------Remove and update

def AES_encrypt(plaintext,key):
    #key=b'0123456789123456'
    nonce=b'B\x1c\x86\xe8Z5Lky\x04\xab.\x96\xf2\xa0\xe5'
    cipher=AES.new(key,AES.MODE_EAX,nonce=nonce)
    utf8_plaintext=bytes(plaintext, 'utf-8')
    ciphertext=cipher.encrypt(utf8_plaintext)
    return (ciphertext)


def AES_decrypt(cipher_text,key):
    #global nonce
    #key=b'0123456789123456'
    #cipher=AES.new(key,AES.MODE_EAX)
    #nonce=cipher.nonce
    nonce=b'B\x1c\x86\xe8Z5Lky\x04\xab.\x96\xf2\xa0\xe5'
    cipher=AES.new(key,AES.MODE_EAX,nonce=nonce)
    plaintext=cipher.decrypt(cipher_text)
    #print(plaintext.decode("utf-8"))######### change RETURN
    return plaintext.decode("utf-8")
    '''
    try:
        cipher.verify(hv)
        print(plaintext.decode("utf-8"))
        return plaintext.decode("utf-8")
    except:
        print("invalid")
        return ""
    '''
