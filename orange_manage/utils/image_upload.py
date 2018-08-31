from upyun import upyun

up = upyun.UpYun("ftp-college-circle", "development", "cxTT9BCjG7AbHioWZsck")


def UploadImg(route, file, headers=None, checksum=False):
    """ 上传文件到又拍云
    :param headers:需要的头信息
    :param checksum:是否进行 MD5 校验
    :param route:上传的路径
    :param file:需要上传的文件对象
    :return:
    """
    try:
        if headers:
            res = up.put(route, file, checksum=checksum, headers=headers)
        else:
            res = up.put(route, file, checksum=checksum)
        return True, res
    except Exception as e:
        return False, str(e)
