import urllib.request, re, os, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

logo_dir = r'C:\Users\DELL\OneDrive\Desktop\LEWS_projectt\LEWS_Project\01022021_website\user_entry\static\images\logos'
os.makedirs(logo_dir, exist_ok=True)

def get_wiki_image(page_title, filename):
    url = f'https://en.wikipedia.org/wiki/{page_title}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
        match = re.search(r'class="infobox-image".*?src="(//upload\.wikimedia\.org/.*?)"', html)
        if match:
            img_url = 'https:' + match.group(1)
            print(f'Found {img_url} for {filename}')
            img_data = urllib.request.urlopen(img_url, context=ctx).read()
            with open(os.path.join(logo_dir, filename), 'wb') as f:
                f.write(img_data)
            print(f'Saved {filename}')
        else:
            print(f'No infobox image found for {page_title}')
    except Exception as e:
        print(f'Error getting {page_title}: {e}')

get_wiki_image('Defence_Research_and_Development_Organisation', 'drdo.png')

# K-DISC Logo from clearbit or direct URL
try:
    kdisc_url = 'https://kdisc.kerala.gov.in/wp-content/themes/kdisc/assets/images/kdisc_logo.png'
    req = urllib.request.Request(kdisc_url, headers={'User-Agent': 'Mozilla/5.0'})
    img_data = urllib.request.urlopen(req, context=ctx).read()
    with open(os.path.join(logo_dir, 'kdisc.png'), 'wb') as f:
        f.write(img_data)
    print('Saved kdisc.png')
except Exception as e:
    print(f'Error getting kdisc.png: {e}')
