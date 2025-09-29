# artposthub
A tool to post your art to multiple websites all at once.

Can also be used as a way to upload a lot of art to one website in succession. For example, posting all of your bunny girl art to your personal website so you don't have to manually click and add each one... with descriptions... and tags... and alt text.. aaaaaaaaaghhhhhhhh


```
usage: autopost.py [-h] [-a ALTTEXT] [-d DESCRIPTION] [-c CAPTION] [--all] [-w] [-b] [-t] title image_path

```

## Currently Supported Modules:

**WordPress:**

* Manually selected using `-w|--wordpress` option.
* Supports adding the title, category, tags, description, and alt text.
* Tags are automatically created if they do not exist.

In `config.py`:
```python
####
## Wordpress Configuration Requirements
####
# The JSON API endpoint for the domain.
wp_url  = 'https://YOUR.DOMAIN.TLD/wp-json/wp/v2'
# The username the key is assigned to.
wp_user = 'WP USERNAME'
# The api key created from within WordPress.
wp_key  = 'WP API KEY'
# The category to upload to.
wp_category = 'art'
# If true, will create tags that do not exist.
wp_create_tag_if_missing = True
```


## Examples:

**Post to all available modules:**
```bash
./autopost.py --all "Penny - Blue Dress" /path/to/penny-blue-dress.png
```

**Post to WordPress only:**
```bash
./autopost.py -w "Penny - Blue Dress" /path/to/penny-blue-dress.png
./autopost.py --wordpress "Penny - Blue Dress" /path/to/penny-blue-dress.png
```

**Post with custom alt text and description:**
```bash
./autopost.py -w -a "A digital painting of a rabbit girl in a blue dress." -d "Penumbra in a rennaisance-ish outfit!" "Penny - Blue Dress" /path/to/penny-blue-dress.png
```

# How does autoposthub automatically obtain tags and alt text from the image?

I'm organizing all of my art images using a [OneFolder](https://github.com/OneFolderApp/OneFolder), a fork of [Allusion](https://github.com/allusion-app/Allusion). OneFolder writes the tags and alt text to the images metadata. This means autoposthub can grab the that data directly from the image.

Unfortunately, this creates a reliance on OneFolder, currently. Since I don't know a friendlier way to keep track of tags and alt text, it'll stay this way until I do. I'll probably do more research to see if there are more standardized ways of doing this.

# Roadmap

## Modules to add:
If possible, I plan to add support for the following websites, in order of priority:
* BlueSky
* Tumblr
* Reddit
* Cara

I do NOT plan to ever add support for:
* X/Twitter

## Features to add:

* Pre-check on the character count for description + tags. If it's over the limit set by BSky, then give a warning.
  * On the same subject, an option to allow for a `--short-description` would probably be nice. That way you could have two separate ones and the modules will decide which to use.
* Flag to disable tags for BSky if you don't want to use hashtags in the description.
* Generalize the tag/alttext metadata retrieval method.
* GUI to make everything easier.
