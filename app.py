#!/usr/bin/env python
# coding: utf-8

# ## Streamlit. Autentication

# Realizamos pruebas para añadir una pantalla de autenticación a una app con streamlit

# In[24]:


import numpy as np
import pandas as pd
import joblib
from io import BytesIO

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# In[25]:


#Realizar hasher de las contraseñas y sustituirlas en config.yaml
#hashed_passwords = stauth.Hasher(['123', '456']).generate()
#hashed_passwords


# In[26]:


#Import the config.yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
#Create the authenticator object:
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#Render the login widget by providing a name for the form and its location (i.e., sidebar or main)
#Con el username podremos implementar privilegios (hacer accesos/app's diferentes según usuario)
name, authentication_status, username = authenticator.login('Login', 'main')


# In[ ]:


#Creamos la función que recibe el df con los datos de las variables y realiza la predicción
def prediccion1 (df):
    ''' Predicción del tipo de erupción volcánica para los valores de un conjunto de registros (data frame)
    ''' 
    model_loaded = joblib.load('best_model.pkl')
    prediccion = model_loaded.predict(df)
    return prediccion    


# In[ ]:


if authentication_status:
    authenticator.logout('Logout', 'main')
    
    #GENERAR LA APP
    st.image('logo_standai.png', width=100)
    st.title('Clasificación de erupciones volcánicas')
    st.markdown('Clasificación del tipo de erupción volcánica en función del valor de 6 sensores de vibración')
    
    st.header('Suba un excel con los valores de los sensores a predecir')
    
    # Permitir descargar un ejemplo de excel
    template= open('Prueba_volcanes.xlsx','rb')
    template_file= template.read()
    st.download_button(
            label='Descargar plantilla ejemplo',
            data= template_file,
            file_name='plantilla_ejemplo.xlsx',
            mime='application/vnd.ms-excel'
        )
    template.close()
    
    # Paso 1: Permitir que el usuario cargue un archivo Excel
    archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx"])
    
    if archivo is not None:
        # Paso 2: Leer el archivo cargado y crear un objeto DataFrame
        df = pd.read_excel(archivo)
        
        # Paso 3: Añadir el campo resultado en el df con la predicción
        df['resultado']= prediccion1(df)
        
        # Paso 4: Convertir el objeto DataFrame en un archivo Excel
        output = BytesIO()
        writer = pd.ExcelWriter(output)
        df.to_excel(writer, index=False )
        writer.close()       
        processed_data = output.getvalue()
        
        # Paso 5: Permitir que el usuario descargue el archivo Excel resultante
        st.download_button(
            label='Descargar archivo Excel',
            data=processed_data,
            file_name='archivo_procesado.xlsx',
            mime='application/vnd.ms-excel'
        )
    
    
    
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

