import sys
import json
import requests
import validators

from bs4 import BeautifulSoup, UnicodeDammit


def validate_image(image):
    if validators.url(str(image)):
        r = requests.head(image)
        if 'image' in r.headers['content-type']:
            return True
    return False


def find_from_srcset(srcset):
    # Working on the assumption that the last image is the best quality
    try:
        for find_url in srcset.split(',')[-1].split(' '):
            if len(find_url) > 5:
                return find_url
    except AttributeError:
        pass


def find_images(soup):
    images = []
    for img in soup.find_all('figcaption'):
        if validate_image(img.find_previous('img').get('src')):
            image_url = img.find_previous('img').get('src')
        else:
            image = find_from_srcset(img.find_previous('img').get('srcset'))
            if validate_image(image):
                image_url = image
            else:
                continue
        images.append({
            img.find_previous('img').get('src'): {
                'caption': img.get_text().strip(),
                'url': image_url
                }
            })
    return images


def generate_content(content):
    response_object = []
    for line in content:
        try:
            response = requests.get(line.strip())
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                response_object.append({
                    'url': line.strip(),
                    'headline': soup.title.string,
                    'images': find_images(soup)
                })
        except ConnectionError as e:
            print(e)
    
    return json.dumps(response_object)


if __name__ == "__main__":

    fo = open("../output/output.json", "w")
    fo.write(
        generate_content(sys.stdin)
        )
    fo.close()
