import requests
from requests.auth import HTTPBasicAuth
import config
import onefolder
 
def upload_image(img_path: str):
    alt_text = onefolder.get_alt_text(img_path)
    tags = onefolder.get_tags(img_path)
    tag_ids = []
    for tag in tags:
        tag_ids.append(get_tag_id(tag))

    url=config.wp_url + '/wp-json/wp/v2/media'
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    filename=img_path.split('/')[-1]

    with open(img_path, 'rb') as image:
        res = requests.post(url=url,
                        data=image.read(),
                        headers={ 'Content-Type': 'image/png','Content-Disposition' : f"attachment; filename={filename}"},
                        auth=auth)
        info = res.json()
        image_info = {
            'id':       info.get('id'),
            'link':     info.get('guid').get('rendered'),
            'alt_text': alt_text,
            'tags': tag_ids
            }
        return image_info

def get_category_id(name):
    url = config.wp_url + "/wp-json/wp/v2/categories?search=" + name
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    
    res = requests.get(url, auth=auth)
    return res.json()[0]['id']

def get_tag_id(name):
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)

    try:
        url = config.wp_url + "/wp-json/wp/v2/tags?search=" + name
        res = requests.get(url, auth=auth)
        return res.json()[0]['id']
    except:
        url = config.wp_url + "/wp-json/wp/v2/tags"
        headers = {"Content-Type": "application/json"}
        post_data = { "name": name }
        res = requests.post(url, auth=auth, headers=headers, json=post_data)
        return res.json()['id']

def post_image(title: str, image_info: str):
    content = f"<!-- wp:image {{'id':{image_info['id']},'linkDestination':'custom','className':'wp-block-image size-large'}} -->\
        <figure class='wp-block-image size-large'>\
        <a href='{image_info['link']}'>\
        <img src='{image_info['link']}' alt='{image_info['alt_text']}' class='wp-image-{image_info['id']}'/>\
        </a></figure>\
        <!-- /wp:image -->"

    content = f"<!-- wp:image {{\"className\":\"size-large\"}} -->\
            <figure class=\"wp-block-image size-large\">\
                <a href=\"{image_info['link']}\">\
                    <img src=\"{image_info['link']}\"/>\
                </a>\
            </figure>\
            <!-- /wp:image -->"

    url = config.wp_url + "/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "featured_media": image_info['id'],
        "tags": image_info['tags'],
        "categories": [get_category_id('art')]
    }

    res = requests.post(url, headers=headers, auth=auth, json=post_data)
    if res.status_code == 201:
        return res.json()
    else:
        return False

def post(title: str, image_path: str):
    image_info = upload_image(image_path)
    json = post_image(title, image_info)
    return json['guid']['rendered']
