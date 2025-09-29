import requests
from requests.auth import HTTPBasicAuth
import config
import onefolder
 
# Uploads the image at the specified image_path.
# Will update with provided alt_text
# and description if provided.
#
# If not provided, it ill attempt to grab alt_text from
# OneFolder information. See onefolder.py
def upload_image(img_path: str, alt_text = '', description=''):
    url=config.wp_url + '/media'
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    filename=img_path.split('/')[-1]

    image_info = None
    with open(img_path, 'rb') as image:
        res = requests.post(url=url,
                        data=image.read(),
                        headers={ 'Content-Type': 'image/png','Content-Disposition' : f"attachment; filename={filename}"},
                        auth=auth)
        image_info = res.json()

    if not alt_text:
        alt_text = onefolder.get_alt_text(img_path)

    if alt_text or description:
        post_data = {
                'alt_text': alt_text,
                'description': description
                }
        res = requests.post(url=url + f"/{image_info['id']}",
                            json=post_data,
                            headers={"Content-Type": "application/json"},
                            auth=auth)
        image_info = res.json()


    return image_info

def get_category_id(name):
    url = config.wp_url + '/categories?search=' + name
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    
    res = requests.get(url, auth=auth)
    return res.json()[0]['id']

# Returns the id of the given tag.
# Will create the tag if it doesn't exist if create_if_missing is
# set to true.
#
# Returns None if the tag doesn't exist and isn't created.
#
# Opinion: I think it should default to true because you can always
# correction a typoed tag in WordPress when you see it. But if it
# doesn't get added at all, you might forget.
def get_tag_id(name: str, create_if_missing: bool = False) -> int:
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    return_id = None

    # Try to return the tag id.
    try:
        url = config.wp_url + '/tags?search=' + name
        res = requests.get(url, auth=auth)
        return_id = res.json()[0]['id']
    # If it doesn't exist, create it and return the new id.
    except:
        print(f"'{name}' doesn't appear to be a valid tag.")
        if create_if_missing:
            print("Creating the tag.")
            url = config.wp_url + '/tags'
            headers = {"Content-Type": "application/json"}
            post_data = { "name": name }
            res = requests.post(url, auth=auth, headers=headers, json=post_data)
            return_id = res.json()['id']

    return return_id

# Return a list of tag ids from strings.
def get_tag_ids(tags: list[str]) -> list[int]:
    return [get_tag_id(tag) for tag in tags if tag]


# Creates a post using a dictionary of an image created by upload_image()
# The data in image_info is the json returned by WordPress
#
# Returns the link of the post.
def post_image(title: str, image_info: str, tag_ids=None) -> str:
    content = f"<!-- wp:image {{\"className\":\"size-large\"}} -->\
            <figure class=\"wp-block-image size-large\">\
                <a href=\"{image_info['link']}\">\
                    <img src=\"{image_info['link']}\"/>\
                </a>\
            </figure>\
            <!-- /wp:image -->"

    if image_info['description']['raw']:
        content += f"<!-- wp:paragraph --><p>{image_info['description']['raw']}</p><!-- /wp:paragraph -->"

    url = config.wp_url + '/posts'
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(config.wp_user, config.wp_key)
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "featured_media": image_info['id'],
        "tags": tag_ids,
        "categories": [get_category_id('art')]
    }

    res = requests.post(url, headers=headers, auth=auth, json=post_data)
    # Returns the URL of the post.
    # TODO: 
    # Currently, if this doesn't work, and exception will be raised.
    # This is good, but will interrupt any future modules being run.
    # Should handle this properly in the future.
    return res.json()['guid']['rendered']

# Uploads an image and creates a WordPress post.
# Returns a link to the post
def post(title: str, image_path: str, tags: list[str] = None, alt_text: str = "", description : str = "") -> str:
    # Upload the image to WordPress.
    image_info = upload_image(image_path, alt_text=alt_text, description=description)

    # Get tag ids from image.
    if not tags:
        tags = onefolder.get_tags(image_path)
    tag_ids = get_tag_ids(tags)

    # Create a post with the image as the main content and featured media.
    post_link = post_image(title, image_info, tag_ids)

    # Return the post link in case you want it.
    return post_link
