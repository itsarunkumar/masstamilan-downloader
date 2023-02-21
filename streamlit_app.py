import streamlit as st
from bs4 import BeautifulSoup
import requests
import wget

# Title
st.title("Masstamilan Downloader")

source_url = "https://masstamilan.dev/music/"

author = st.selectbox("Select the language", [
    "anirudh-ravichander"])

st.write("You selected:", author)

url = source_url + author


def getContent(url):
    refined_content_lst = []
    content = requests.get(url)
    print(content.status_code)
    print(content.url)
    content = content.content
    content = BeautifulSoup(content, "html.parser")
    # f_content = content.select('.botlist')
    refined_content = content.select('div.a-i > a')
    for i in refined_content:
        print(i['href'])
        refined_content_lst.append(i['href'])
    return refined_content_lst


refined_list = getContent(url)

st.write(refined_list)


url2 = "https://masstamilan.dev"


def getSongurl(url, refined_content_lst):
    song_url = []
    for i in refined_content_lst:
        sm = requests.get(url+i)
        song_url.append(sm.url)
        sm = BeautifulSoup(sm.content, "html.parser")

    return song_url


song_url = getSongurl(url2, getContent(url))

st.write(song_url)


def getDownloadUrl(op):
    songlist = []
    for i in op:
        sm = requests.get(i)
        sm = BeautifulSoup(sm.content, "html.parser")
        for link in sm.find_all('a'):
            if link.get('href').startswith('/downloader'):
                if 'umami--click--dl320' in link.get('class'):
                    songlist.append(link.get('href'))

    return songlist


songlist = getDownloadUrl(song_url)

st.write(songlist)


def downloadSong(songlist, url2):
    songlist = songlist[:3]
    for i in songlist:
        d_url = url2 + i
        # print(d_url)
        fd_url = requests.get(d_url)
        print(fd_url.url)
        wget.download(fd_url.url)


if st.button("Download"):
    downloadSong(songlist, url2)
