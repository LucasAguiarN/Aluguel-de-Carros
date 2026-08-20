import urllib.request
import traceback

urls = ['http://127.0.0.1:5500/index.html','http://localhost:5500/index.html']
for u in urls:
    print('---', u)
    try:
        r = urllib.request.urlopen(u, timeout=5)
        status = getattr(r, 'status', None)
        body = r.read(200)
        print('STATUS:', status)
        print('LENGTH:', len(body))
        print('HEAD:', body.decode('utf-8','replace')[:200])
    except Exception as e:
        print('ERROR:', e)
        traceback.print_exc()
