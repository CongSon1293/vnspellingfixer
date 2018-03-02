import math

import editdistance

import utils

def cal_matching_first_char(src,cand):
    part1 = src.split(" ")
    part2 = cand.split(" ")
    s1 = len(part1)
    s2 = len(part2)
    sz = min(s1,s2)
    first_score = 0.1
    total_score = 0
    try:
        for i in xrange(sz):
            if part1[i][0] == part2[i][0]:
                total_score += first_score /(i+1)
    except:
        pass
    return total_score

def cal_sim_score(src, cand, ref_score=0):
    l = 0.5*(1.0/len(src)+1.0/len(cand))
    count = utils.lcs2(src, cand) * 1.0 + 1.05 + math.log(1.0 / (1.2 + editdistance.eval(src, cand)))

    #if src[0] == cand[0]:
    #    count += 0.1
    count += cal_matching_first_char(src,cand)
    if ref_score > 0:
        count += math.log(100.0 + ref_score) / math.log(1000)
    return count *l

def cal_sim_score_2(src,cand,ref_score=0):
    dc = len(src) * 1.0
    count = utils.lcs2(src, cand) * 1.0
    if src[0] == cand[0]:
        count += 0.1
    count += math.log(100.0 + ref_score) / math.log(1000)
    return count / dc
