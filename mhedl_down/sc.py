#!/usr/bin/env python

'''
Sample usage:
python sc.py renai_boukun Renai_Boukun_Manga
'''
import requests, sys, os
import bs4
import ssl
import subprocess

manga_name = sys.argv[1] # the part after mp_url_base
manga_foldername = sys.argv[2]

mp_url_base = "https://www.mangahere.co/manga/"

mp_url = mp_url_base + manga_name
mp_fname = manga_name + ".html"

DEBUG = True
def downloadSingleChapter(c_link):
    
    # phase one : make dir
    
    i = c_link.index(manga_name)
    # get the c[num] part, excluding the bounding /'s
    #foldername = c_link[i + len(manga_name) + 1:-1]
    foldername = c_link[-5:-1]
    
    full_p = os.path.join(manga_foldername, foldername)

    try:
        os.mkdir(full_p)
    except:
        pass

    #phase 2: download pages
    #increment page number until you get 404
    pnum = 1

    while True:
        
        p_link = "https:" + c_link + str(pnum) + ".html"
        r = requests.get(p_link, verify=False)
        
        if DEBUG:
            print("RINKO : {}".format(p_link))

        # exit when pages are exhausted
        '''
        if r.status_code != 200:
            print("Chapter completed.")
            break
        '''
        if 'error_404' in r.text:
            print('Chapter completed.')
            break



        # write page's html file
        html_path = os.path.join(full_p, str(pnum) + ".html")
        with open(html_path, 'wb') as f:
            f.write(r.content)

        f = open(html_path, 'r')
        soup = bs4.BeautifulSoup(f.read())
        f.close()

        # get image
        img_link  = ''
        for img in soup.find_all('img'):
            #if img.has_attr('onload') and img['onload'] == ['loadImg(this)']:
            if img.has_attr('onload'):
                img_link = img['src']
                if DEBUG:
                    print("IMAGE: {}".format(img_link))

        # download the image
        ir = requests.get(img_link, verify=False)
        assert ir.status_code == 200

        #NOTE: have assumed jpeg
        img_path = os.path.join(full_p, str(pnum) + ".jpg")
        with open(img_path, 'wb') as f:
            f.write(ir.content)

        # remove html
        os.remove(html_path)

        pnum += 1


def downloadChapters(chap_li, suru, khatam):
    
    for ind in range(suru, khatam+1):
        
        chapter_link = chap_li[ind]
        print("Downloading chapter {}".format(ind))
        downloadSingleChapter(chapter_link)

def main():
    
    # make dir
    try:
        os.mkdir(manga_foldername)
    except:
        pass

    # Download main page
    r = requests.get(mp_url, verify=False)
    assert r.status_code == 200

    with open(mp_fname, 'wb') as f:
        f.write(r.content)

    # Read page and create bs4 object
    f = open(mp_fname, 'r')
    soup = bs4.BeautifulSoup(f.read())
    f.close()

    # obtain list of chapter urls
    chap_li = []
    for a in soup.find_all('a'):
        if a.has_attr('href') and manga_name in a['href']:
            # filter out comments and main page
            if 'comments' not in a['href'] and 'm.mangahere' not in a['href']:
                chap_li.append(a['href'])

    chap_li.reverse()

    print('Chapter list: ')
    for each in chap_li:
        print (each)

    print('Total number of chapters: {}'.format(len(chap_li)))

    dl_start = int(input(">>Enter DL start list index: "))
    dl_stop = int(input(">>Enter DL stop list index: "))

    downloadChapters(chap_li, dl_start, dl_stop)

if __name__ == '__main__':
    main()
