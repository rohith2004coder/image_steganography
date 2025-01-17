import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import sys
from base64 import b64encode

###################
import steganography as stg
from PIL import Image
###################

################################### Key Exchange Part ############################################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.82.172', 5000))
server.listen()

client, client_address = server.accept()

pem_data=client.recv(2048)
key = RSA.import_key(pem_data)
if key.publickey():
    print("PUBLIC KEY RECEIVED IS:")
    print(f"Public Key (n, e): ({key.n}, {key.e})")
    print("\n")

#encryption of aes key
aes_key = os.urandom(16)

#printing the aes key generated
print("The AES key generated is:"+b64encode(aes_key).decode('utf-8'))
print("\n")

rsa_cipher=PKCS1_OAEP.new(key)
aes_key_cipher=rsa_cipher.encrypt(aes_key)
#print(sys.getsizeof(aes_key_cipher))

#sending encrypted aes_key
cipher_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cipher_socket.connect(('192.168.82.75', 6000))

cipher_socket.send(aes_key_cipher)
client.close() 
server.close()
################################## Sending Image ################################################

client_img=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_img.connect(('192.168.82.75', 5000))

#-------------------------------------#
plaintext=str(input("Enter plaintext: "))
cover_image=str(input("Enter cover image (filename.extension): "))
cipher_text=stg.AES_encrypt(plaintext,aes_key)

print("Cipher text generated by AES is: ",cipher_text)####----------------------debug remove
#img=Image.open('image_crypt.jpg')
img=Image.open(cover_image)
'''
#--#
px=img.load()
for i in range(10):
  print(px[i,0],end=' , ')
print()
#--#
'''
stg.encode_img(img,cipher_text)
'''
#--#
px=img.load()
for i in range(10):
  print(px[i,0],end=' , ')
print()
#--#
'''
img.save('encoded_image.png')
encode_img=Image.open('encoded_image.png')
'''
#--#
px=encode_img.load()
for i in range(10):
  print(px[i,0],end=' , ')
print()
#--#
'''
img.close()
#-------------------------------------#


file=open('encoded_image.png','rb')

image_data=file.read(2048)

while image_data:
  client_img.send(image_data)
  image_data=file.read(2048)

file.close()
client_img.close()