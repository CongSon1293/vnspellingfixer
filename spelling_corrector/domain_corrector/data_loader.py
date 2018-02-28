import os
from io import open
FPT_SHOP_MOBILE_DATA_FILE = "fpt_shop_mobile.dat"
DATA_ROOT = "/home/nda/Data/Data_NLP"

def get_fpt_mobile_data_file_reader():
    f = open("%s/%s" % (DATA_ROOT,FPT_SHOP_MOBILE_DATA_FILE), "r", encoding="utf-8")
    return f