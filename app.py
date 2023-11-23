#!/usr/bin/env python
# coding: utf-8

# # Web para predicción de volcanes (con Streamlit)

# - Recuperamos el modelo con la librería joblib
# - Generamos una app con streamlit. Creamos archivo .py
# - La subimos a la nube de streamlit y hacemos pruebas

# In[1]:


#Libraries
import numpy as np
import pandas as pd
import joblib
import streamlit as st


# In[4]:


#Creamos la función que recibe los datos de las variables (sin sus nombres y un sólo registro)
#Se puede crear en un archivo independiente (prediction.py) y luego en la librería añadir: from prediction import prediccion1

def prediccion1 (feature1, feature2, feature3, feature4, feature5, feature6):
    ''' Predicción del tipo de erupción volcánica para los valores
    de un solo registro'''
    
    model_loaded = joblib.load('best_model.pkl')
    data= pd.DataFrame({'feature1': feature1,
                    'feature2': feature2,
                    'feature3': feature3,
                    'feature4': feature4,
                    'feature5': feature5,
                    'feature6': feature6},
                      index=[0])
    prediccion = model_loaded.predict(data)[0]
    return prediccion    


# In[5]:


# We create the main function in which we define our webpage. We create the streamlit componets
def main():
    st.title('Erupciones volcánicas')
    st.markdown('Clasificación del tipo de erupción volcánica en función del valor de 6 sensores de vibración')
    
    st.header('Sensores de vibración')
    col1, col2 = st.columns(2)
    with col1:
        st.text('Variables tipo A')
        feature1 = st.slider('feature1', -2.0, 5.0, 0.5)
        feature2 = st.slider('feature2', -2.0, 5.0, 1.5)
        feature3 = st.text_input('feature3') 
    with col2:
        st.text('Variables tipo B')
        feature4 = st.text_input('feature4')
        feature5 = st.text_input('feature5')
        feature6 = st.text_input('feature6')
    result =""
    
    if st.button("Predict"): 
        result = prediccion1(feature1, feature2, feature3, feature4, feature5, feature6) 
    st.success('El tipo de erupción es {}'.format(result)) 

if __name__=='__main__': 
    main() 

