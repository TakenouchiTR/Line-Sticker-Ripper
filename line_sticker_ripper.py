#!/usr/bin.env python3

import os
import re
import requests
import threading

VERSION = '1.0'
regex_url = r'^https://store.line.me/stickershop/product/\d*/\w*/?$'
regex_title = r'<p class="mdCMN38Item01Ttl">(.*)</p>'
regex_image = r'background-image:url\(([\w\d:/\.\-]*);'
sticker_folder = ''

def main():
    line_url = get_url()

    data = requests.get(line_url)
    byte_arr = data.content
    html_string = byte_arr.decode('utf8')

    title = re.search(regex_title, html_string).group(1)
    images = re.findall(regex_image, html_string)
    download_folder = os.path.join(sticker_folder, title)

    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    print('Downloading {} images to .../stickers/{}/'.format(
        len(images) // 2, title))

    for i in range(0, len(images), 2):
        download_thread = threading.Thread(target=download_image, 
          args=(images[i],'{}{}.png'.format(download_folder, str(i // 2))))
        download_thread.start()
        download_thread.join()
    
    input('Download complete. Please press enter to close.')

def download_image(image_url, file_name):
    data = requests.get(image_url)
    file = open(file_name, 'wb')
    file.write(data.content)
    file.close()


def get_url():
    line_url = ''
    valid_url = False

    while not valid_url:
        line_url = input('Enter the sticker URL: ')

        if re.search(regex_url, line_url) == None:
            print('Url is not valid.')
            print('Please input the entire URL for the store page' +
              '(https://store.line.me/stickershop/product/<id>/)\n')
        else:
            valid_url = True

    return line_url
    

if __name__ == '__main__':
    sticker_folder = os.path.join(os.getcwd(), 'stickers')
    if not os.path.exists(sticker_folder):
        os.mkdir(sticker_folder)

    main()