import re
SPLITER_TOKENS = re.compile(ur"($|\.\.\.)|(\!\!\!)|\.|\,|\?|\!|\;",re.UNICODE)
sen = "Toi muon di choi. Ban co muon khong dc? the thi tot."


def __split_segment_sentence( sen):
    mo_segments = SPLITER_TOKENS.finditer(sen)
    segments = []
    spliters = []
    start_index = 0
    for mo in mo_segments:
        segment = sen[start_index:mo.start()]
        spliter = mo.group(0)
        start_index = mo.start() + len(spliter)
        segments.append(segment)
        spliters.append(spliter)

    return segments, spliters

print __split_segment_sentence(sen)