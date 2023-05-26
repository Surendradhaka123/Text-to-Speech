import streamlit as st
import time
from datetime import datetime
from transformers import SpeechT5Processor, SpeechT5ForSpeechToSpeech, SpeechT5HifiGan,SpeechT5ForTextToSpeech
import numpy as np
import torch
from io import StringIO
import soundfile as sf


html_temp= """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:centre;"> Text-to-Speech </h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

st.markdown(
   
    """
    This is an AI tool. This tool will convert your text into audio. You can also drop you text file here and download the audio file.
"""
)
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

speaker_embeddings = np.load("cmu_us_slt_arctic-wav-arctic_a0499.npy")
speaker_embeddings = torch.tensor(speaker_embeddings).unsqueeze(0)

text = st.text_area("Type your text..")
st.button("Convert")
inputs = processor(text=text, return_tensors="pt")
spectrogram = model.generate_speech(inputs["input_ids"], speaker_embeddings)
with torch.no_grad():
    speech = vocoder(spectrogram)
    sf.write("speech.wav", speech.numpy(), samplerate=16000)
    
audio_file = open('speech.wav', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/wav')


uploaded_file=st.file_uploader("Upload your text file here",type=['txt'] )
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #To read file as string:
    text = stringio.read()
    st.write(text)
    
    st.button("Convert",key=1)
    inputs = processor(text=text, return_tensors="pt")
    spectrogram = model.generate_speech(inputs["input_ids"], speaker_embeddings)
    with torch.no_grad():
        speech = vocoder(spectrogram)
        sf.write("speech.wav", speech.numpy(), samplerate=16000)
    audio_file = open('speech.wav', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
    
    
    
    
    
st.text("Thanks for using")
            
if st.button("About"):
        st.text("Created by Surendra Kumar")
## footer
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="solid",
        border_width=px(0.5)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )
    st.markdown(style,unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "©️ surendraKumar",
        br(),
        link("https://www.linkedin.com/in/surendra-kumar-51802022b", image('https://icons.getbootstrap.com/assets/icons/linkedin.svg') ),
        br(),
        link("https://www.instagram.com/im_surendra_dhaka/",image('https://icons.getbootstrap.com/assets/icons/instagram.svg')),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()
