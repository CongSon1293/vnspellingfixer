import utils
import math
import editdistance
def cal_sim_score(src, cand, ref_score=0):
    l = 0.5*(1.0/len(src)+1.0/len(cand))
    count = utils.lcs2(src, cand) * 1.0 + 1.05 +  math.log(1.0/(1.2+ editdistance.eval(src,cand)))

    if src[0] == cand[0]:
        count += 0.1
    if ref_score > 0:
        count += math.log(100.0 + ref_score) / math.log(1000)
    return count *l
