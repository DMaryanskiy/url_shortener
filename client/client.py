import requests
import streamlit as st

BACKEND = 'http://backend:80/api/v1/url/'

st.title('URL Shortener service')

st.write(
    '''
    Small API which helps to shorten your enourmous big url to a moew tiny one.
    Just put your url in a form and it'll generate small uri for it.
    Also you may provide your own uri to get your custom link
    '''
)

original_link = st.text_input(label='Original link', placeholder='Put your large link here')
short_link = st.text_input(label='Short link', placeholder='Put here your custom uri (optional)')

if st.button(label='Submit data'):
    try:
        json = {
            'original_url': original_link,
        }
        if len(short_link):
            json['short_uri'] = short_link
        response= requests.post(BACKEND + 'shorten', json=json)
        data = response.json()
    except Exception as exc:
        st.text(f'Something went wrong :(\nReason: {exc}')
    else:
        st.text('Your short link:')
        st.code(data['short_uri'])
