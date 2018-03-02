import os
from io import open
import unicodedata
import json
FPT_SHOP_MOBILE_DATA_FILE = "fpt_shop_mobile.dat"
DATA_ROOT = "/home/nda/Data/Data_NLP"
DATA_DIR = "/home/nda/Data/Data_NLP"

cdir = os.path.abspath(os.path.dirname(__file__))



def export_question_answer_sentences(using_answer=False):
    '''
        Product data structure:
        Json:
        {
            title: "Title"
            {key-property: Ram, CPU,Monitor...} : "Value"
            commments: List-Of-Question-Answer-Pairs:[[Q1,A1],[Q2,A2],[Q3,A3],...]
        }
    '''
    import re
    re_ldots = re.compile("\.\.\.", re.UNICODE)
    re_markers = re.compile("[?,;!]")
    re_dotspace = re.compile("\.")

    def norm_paragraph(para):
        para = unicodedata.normalize("NFKC",para)
        para = para.replace("\r","")
        para = para.replace("\n",". ")
        para = re_ldots.sub(".",para)
        para = re_markers.sub(".",para)
        para = re_dotspace.sub(" . ",para)
        return para
    def split_paragraph(para):
        sentences = para.split(" . ")
        return sentences

    def export():
        fin = open("%s/data/inp/fpt_mobiles_product_and_qa.dat" % cdir, "r")
        fout = open("%s/fpt_shop_mobile.dat"%DATA_DIR,"w",encoding="utf-8")

        while True:
            line = fin.readline()
            if line == "":
                break
            s = json.loads(line.strip())
            try:
                title = s['title']
                qas = s['comments']
                for qa in qas:
                    try:
                        question = qa[0]
                        para = norm_paragraph(question)
                        sentences = split_paragraph(para)
                        for sen in sentences:
                            sen = sen.strip()
                            if len(sen) < 3:
                                continue

                            fout.write(u"%s\n"%sen)
                    except:
                        pass
                    if using_answer:
                        try:
                            answer = qa[1]

                            para = norm_paragraph(answer)
                            sentences = split_paragraph(para)
                            for sen in sentences:
                                sen = sen.strip()
                                if len(sen)<3:
                                    continue
                                fout.write(u"%s\n"%sen)
                        except:
                            pass


            except Exception as e:
                continue

        fin.close()
        fout.close()
    export()

def get_fpt_mobile_data_file_reader():
    f = open("%s/%s" % (DATA_ROOT,FPT_SHOP_MOBILE_DATA_FILE), "r", encoding="utf-8")
    return f
if __name__ == "__main__":
    export_question_answer_sentences(using_answer=True)