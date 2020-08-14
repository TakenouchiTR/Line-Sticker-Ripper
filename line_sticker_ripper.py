import os
import re
import urllib.request

regex_url = r'^https://store.line.me/stickershop/product/\d*/\w*$'
regex_title = r'mdCMN38Item01Ttl">([a-zA-Z0-9 !/;,\\\.\-\?\+\*]*)</p>'
regex_image = r'background-image:url\(([\w\d:/\.\-]*);'

def main():
    line_url = get_url()

    data = urllib.request.urlopen(line_url)
    byte_arr = data.read()
    html_string = byte_arr.decode('utf8')

    title = re.match(regex_title, html_string)
    images = re.findall(regex_image, html_string)

    folder = 'stickers/{}/'.format(title)

    for i in range(0, len(images), 2):
        download_image(images[i], '{}{}.png'.format(folder, str(i // 2)))

def download_image(image_url, file_name):
    data = urllib.request.urlopen(image_url)

    file = open(file_name, 'wb')


def get_url():
    line_url = ''
    valid_url = False

    while not valid_url:
        line_url = input('Enter the sticker URL: ')

        if re.search(regex_url, line_url) == None:
            print('Url is not valid.')
            print('Please input the entire URL for the store page (https://store.line.me/stickershop/product/<id>/<lang>)\n')
        else:
            valid_url = True

    return line_url
    

if __name__ == '__main__':
    if not os.path.exists('/stickers/'):
        os.mkdir('/stickers/')

    main()