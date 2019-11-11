import pyqrcode
import base64
import io 
def gen_qr(l):
    ''' Generates a qr code based on the parameters passed in the form of a list'''
    url = pyqrcode.create(l)
    return url

def qrencode64(url):
    buffer = io.BytesIO()
    #url.svg(buffer)
    url.svg(buffer)
    b64 = base64.b64encode(buffer.getvalue())
    return b64
    
