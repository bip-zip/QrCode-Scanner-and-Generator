from django.views.generic import TemplateView
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
from django.http import HttpResponse


class QrCodeView(TemplateView):
    template_name='qr.html'

    def get_context_data(self, **kwargs):
        context = super(QrCodeView, self).get_context_data(**kwargs)
        # fill your data here
        qrcode =  self.get_qrcode_svg('{}&{}'.format('This is the qrcode data guys.','bip-zip'))
        context.update({"qrcode":qrcode})
        return context
    
    def get_qrcode_svg(self, text):
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(text ,image_factory=factory, box_size=30)
        stream = BytesIO()
        img.save(stream)
        base64_image = base64.b64encode(stream.getvalue()).decode()
        return 'data:image/svg+xml;utf8;base64,' + base64_image


class QrCodeScan(TemplateView):
    template_name= 'qrscanner.html'

    def post(self,request):
        image = request.POST['image']
        image_data = base64.b64decode(image.split(',')[1])

        img = BytesIO(image_data)
        data = self.qrcodeReader(img)
        if data == False :
            # your error message
            return HttpResponse('No Qr code found! Sorry.')
        return HttpResponse(data)
        # send data whereever you want :
        # return redirect("/add/?qrdata={}".format(data))
    
    def qrcodeReader(self, img):
        # Read the image data using Pillow
        image = Image.open(img)
        # Convert the image to grayscale
        gray_image = image.convert('L')
        # Convert the grayscale image to a NumPy array
        np_image = np.array(gray_image)
        # Decode the QR code in the image using pyzbar
        decoded = decode(np_image)
        # Get the data from the QR code
        if len(decoded) > 0:
            data = decoded[0].data.decode('utf-8')
        else:
            data = False
        return data
        
    



