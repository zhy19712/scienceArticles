from hashlib import sha1

from djangoProject.settings import SECRET_KEY


def make_password(password):
    # 1.加盐,SECRET_KEY为加盐字符串,from ads.settings import SECRET_KEY
    password = SECRET_KEY + password
    # 2.开始加密
    sha1_obj = sha1()
    sha1_obj.update(password.encode())
    ret = sha1_obj.hexdigest()

    # sha1,md5两种加密算法类似,sha1加密后40位,md5加密后32位,sha1相对安全,但速度慢
    # md5_obj = md5()
    # md5_obj.update(password.encode())
    # ret = md5_obj.hexdigest()
    # print(ret)  # 201812424099946c9c5590be9754b94b
    # print(len(ret))  # 32
    return ret
