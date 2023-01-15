import os


def creat_md5(file_path: str) -> str:
    os.system(
        "certutil -hashfile {file_path} MD5 > {md5_path}".format(file_path=file_path, md5_path=file_path + ".md5"))
    md5_path = file_path + ".md5"
    md5 = open(md5_path, "r")
    md5_code = md5.readlines()[1].strip()
    md5.close()
    return md5_code


def md5_align(md51, md52) -> bool:
    if md51 == md52:
        return True
    else:
        return False
