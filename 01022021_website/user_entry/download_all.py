import urllib.request, re, os, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

logo_dir = r'C:\Users\DELL\OneDrive\Desktop\LEWS_projectt\LEWS_Project\01022021_website\user_entry\static\images\logos'
os.makedirs(logo_dir, exist_ok=True)

def download_file(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data = urllib.request.urlopen(req, context=ctx).read()
        with open(os.path.join(logo_dir, filename), 'wb') as f:
            f.write(img_data)
        print(f'Successfully saved {filename}')
    except Exception as e:
        print(f'Failed {filename}: {e}')

# NMHS logo
download_file('https://nmhs.org.in/img/logo.png', 'nmhs.png')

# DRDO logo
download_file('https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Defence_Research_and_Development_Organisation.svg/250px-Defence_Research_and_Development_Organisation.svg.png', 'drdo.png')

# K-DISC logo
download_file('https://kdisc.kerala.gov.in/wp-content/themes/kdisc/assets/images/kdisc_logo.png', 'kdisc.png')

# ISRO logo
download_file('https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Indian_Space_Research_Organisation_Logo.svg/512px-Indian_Space_Research_Organisation_Logo.svg.png', 'isro.png')
