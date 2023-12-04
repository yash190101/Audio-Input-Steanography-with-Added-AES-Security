import streamlit as st
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy
import random
import string
from Crypto.Cipher import AES
from pydub import AudioSegment
from PIL import Image
def HomePage():
    st.sidebar.markdown("Home Page")
    st.header("AUDIO IN AUDIO STEGANOGRAPHY")
    st.write(": Group Members :")
    st.write(" 1) Nidhi Karulkar ")
    st.write(" 2) Ruchali Mhatre ")
    st.write(" 3) Yash Patil ")
    st.write(": Guide :")
    st.write(" Prof. Anil Hingmire ")


def Encryption():
    st.header("Upload File for Encryption And Encoding")
    st.sidebar.markdown("# Encryption And Encoding")
    uploaded_file = st.file_uploader("Choose a file")
    st.text("")
    

    if uploaded_file:
      
      st.write('Your Uploaded File :')
      image = Image.open('og_aduio_plot.png')
      st.image(image)
      st.write("After performing Encryption and Encoding:")
      st.text("")
      file_name = uploaded_file.name
      
      
      fs, data = wavfile.read('secret.wav')
      with open('secret.wav', 'rb') as fd:
        contents = fd.read()
      AES_KEY,AES_IV=aes()

      encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
      encrypted_audio = encryptor.encrypt(contents)

      with open('encrypted_audio_file.txt', 'wb') as fd:
        fd.write(encrypted_audio)
      
      with open('encrypted_audio_file.txt', 'rb') as fd:
        contents1 = fd.read()
      
      bits = ''.join(format(b, '08b') for b in contents1)
      
      song = wave.open("cover.wav", mode='rb')

      frame_bytes = bytearray(list(song.readframes(song.getnframes())))

      for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)
        # Get the modified bytes
      frame_modified = bytes(frame_bytes)

      with wave.open('song_embedded.wav', 'wb') as fd:
          fd.setparams(song.getparams())
          fd.writeframes(frame_modified)
      song.close()

      audio_file = open('song_embedded.wav', 'rb')
      audio_bytes = audio_file.read() 
      st.audio(audio_bytes, format='audio/wav')

      st.write("Click on options to download the file")

      st.write(': Your secret key :')
      st.write(AES_KEY)




def Decryption():
    st.header("Upload File for Decryption and Decoding")
    st.sidebar.markdown("# Decryption and Decoding")
    uploaded_file1 = st.file_uploader("Choose a file")
    st.text("")
    if uploaded_file1:
      
      st.write('Your Uploaded File :')
      image = Image.open('audiofordecryption.png')
      st.image(image)

      key_decryption = st.text_input('Enter Your Secret Key: ', '')
      AES_KEY,AES_IV=aes()
      if key_decryption :
        st.write("After performing Decoding and Decryption:")
        st.text("")
        file_name = uploaded_file1.name
      
      
        song = wave.open("song_embedded.wav", mode='rb')
        # Convert audio to byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
      
        listToStr = ''.join([str(elem) for elem in extracted])
      
        n = int(listToStr, 2)

        num_bytes = (len(extracted) + 7) // 8
        byte_data = n.to_bytes(num_bytes, byteorder='big')
      
        decryptor = AES.new(key_decryption.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
        decrypted_audio = decryptor.decrypt(byte_data)

        with open('decrypted_audio_file1.wav', 'wb') as fd:
          fd.write(decrypted_audio)
      

        audio_file = open('decrypted_audio_file1.wav', 'rb')
        audio_bytes = audio_file.read() 
        st.audio(audio_bytes, format='audio/wav')


        st.write("Click on options to download the file")



def aes():
    AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

    AES_IV = 'huPuVAIQE1WpOMfp'
    return(AES_KEY,AES_IV)



page_names_to_funcs = {
    "Home Page": HomePage,
    "Encryption": Encryption,
    "Decryption": Decryption,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()