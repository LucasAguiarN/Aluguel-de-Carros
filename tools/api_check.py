import urllib.request
import urllib.error
import json

BASE = 'http://127.0.0.1:5000'
ENDPOINTS = ['/', '/veiculos', '/veiculos/disponiveis', '/clientes']

for ep in ENDPOINTS:
    url = BASE + ep
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            status = getattr(r, 'status', None)
            body = r.read()
            print('---', url)
            print('status:', status)
            try:
                parsed = json.loads(body.decode('utf-8'))
                print(json.dumps(parsed, ensure_ascii=False, indent=2)[:1000])
            except Exception:
                print('body (text):', body.decode('utf-8','replace')[:1000])
    except urllib.error.HTTPError as he:
        print('---', url)
        print('HTTP ERROR:', he.code, he.reason)
        try:
            print(he.read().decode('utf-8','replace')[:1000])
        except Exception:
            pass
    except Exception as e:
        print('---', url)
        print('ERROR:', e)
