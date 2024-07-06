import socket
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
from base64 import b64encode

#########################################
import steganography as stg
from PIL import Image
#########################################

#######################  Key Exchange ################################################

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.public_key().export_key()

#sending public key

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.82.75', 5000))
client.send(public_key)

#recieving cipher text

cipher_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cipher_socket.bind(('192.168.82.172', 6000))
cipher_socket.listen()

cipher_recv_socket, cipher_recv_addr=cipher_socket.accept()

aes_cipher=cipher_recv_socket.recv(1024)

#decryption

rsa_cipher=PKCS1_OAEP.new(RSA.import_key(private_key))
aes_key=rsa_cipher.decrypt(aes_cipher)

print("The AES key recieved is:"+b64encode(aes_key).decode('utf-8'))

client.close()

################# Recieving image #############################################################
server_img=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_img.bind(('192.168.82.172', 5000))

server_img.listen()

client, client_address=server_img.accept()

file=open('server_image.png','wb')

image_data=client.recv(2048)

while image_data:
  file.write(image_data)
  image_data=client.recv(2048)

file.close()

#---------------------------------------------------#
img=Image.open('server_image.png')
cipher_text=stg.decode_img(img)
print("Cipher text decoded from image is: ",cipher_text)######------------------debug remove
plaintext=stg.AES_decrypt(cipher_text,aes_key)#####################    ADD
print("Secret Text enclosed in image is:")
print(plaintext)#####################    ADD
#---------------------------------------------------#

client.close()
