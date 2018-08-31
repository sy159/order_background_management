# _author:"CyJay"
# _date:2018/8/30
from datetime import datetime

from orange_manage.utils.image_upload import UploadImg

a = open('46715c54ecac4aa.jpg', 'rb')

b, c = UploadImg("/static/illustratio/46715c54ecac4aa.jpg", a)
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(b)
print(c)
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
