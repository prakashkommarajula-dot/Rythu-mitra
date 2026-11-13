import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

opener = urllib.request.build_opener()

# 1. Test POST /api/set-language
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/set-language',
    data=json.dumps({'language': 'en'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
resp = opener.open(req)
print("1. Set-Language POST:", resp.status, resp.read().decode('utf-8').strip())
print("   Set-Cookie:", resp.headers.get('Set-Cookie'))

# 2. Test Advisory English
resp_en = opener.open('http://127.0.0.1:5000/advisory?disease=Blast&crop=Rice&lang=en')
html_en = resp_en.read().decode('utf-8')
print("2. Advisory EN Status:", resp_en.status)
print("   Has <html lang=\"en\">:", '<html lang="en">' in html_en)
print("   Has 'Overview, Pathogen Biology':", "Overview, Pathogen Biology" in html_en)

# 3. Test Advisory Telugu
resp_te = opener.open('http://127.0.0.1:5000/advisory?disease=Blast&crop=Rice&lang=te')
html_te = resp_te.read().decode('utf-8')
print("3. Advisory TE Status:", resp_te.status)
print("   Has <html lang=\"te\">:", '<html lang="te">' in html_te)
print("   Has Telugu text:", "సమగ్ర సస్యరక్షణ" in html_te or "అగ్గి తెగులు" in html_te or "తెగులు" in html_te)

# 4. Test Home page
resp_home = opener.open('http://127.0.0.1:5000/')
print("4. Home Status:", resp_home.status)

# 5. Test Predict page
resp_pred = opener.open('http://127.0.0.1:5000/predict')
print("5. Predict Status:", resp_pred.status)
