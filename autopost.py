import wordpress
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("title", help="The title for the post.", type=str)
parser.add_argument("image_path", help="The path to the image file.", type=str)
parser.add_argument("-a", "--alttext", help="Alt text for the image.", type=str)
parser.add_argument("-d", "--description", help="A description for the image.", type=str)
parser.add_argument("-c", "--caption", help="A caption for the image.", type=str)
parser.add_argument("--all", help="Enables all available modules.", action="store_true")
parser.add_argument("-w", "--wordpress", help="Enables the WordPress module.", action="store_true")
parser.add_argument("-b", "--bluesky", help="Enables the WordPress module.", action="store_true")
parser.add_argument("-t", "--tumblr", help="Enables the WordPress module.", action="store_true")
args = parser.parse_args()

if args.all:
    args.wordpress = True
    args.bluesky = True
    args.tumblr = True

if args.wordpress:
    try:
        link = wordpress.post(args.title, args.image_path, description=args.description, alt_text=args.alttext)
        print("WordPress Post URL: " + link)
    except Exception as e:
        print("ERROR: There was an issue posting to WordPress.")
        print(f"Title: {args.title}")
        print(f"Image Path: {args.image_path}")
        print(e)

