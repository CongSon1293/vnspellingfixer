# Sửa lỗi chính tả không dấu
# Thuật toán học không giám sát
## Input - Output
```
Input: 
	- Tập luật thay thế có trước
	- Bộ từ điển chuẩn (gồm có dấu và không dấu)
	- Bộ dữ liệu của miền cần sửa chữa

Output:
	- Bộ sửa lỗi chính tả
```

## Khái niệm từ sai
```
Từ sai là từ thõa mãn các điều kiện sau:
	- Chữ cái đầu tiên không viết hoa
	- Dạng không dấu của nó không nằm trong bộ từ điển không dấu
```

## Khoảng các giữa hai từ:
### Khoảng cách sửa lỗi (editditance)
```
Là số lần sửa lỗi tối thiểu (thêm sửa xóa) để biến xâu này thành xâu kia
package editdistance python

Kí hiệu d1
```
### Xâu con chung dài nhất (có tính thứ tự)
```
Keyword: longest common subsequence
Kí hiệu l1

```

### Khoảng cách hai từ:
Xem file similarity_metrics.py
```
def cal_matching_chars(src,cand):
    part1 = src.split(" ")
    part2 = cand.split(" ")
    s1 = len(part1)
    s2 = len(part2)
    sz = min(s1,s2)
    first_score = 0.1
    total_score = 0
    matching_word_score = 0
    try:
        for i in xrange(sz):
            if part1[i][0] == part2[i][0]:
                total_score += first_score /(i+1)
            if part1[i] == part2[i]:
                matching_word_score + first_score /(i+1)
    except:
        pass
    return total_score,matching_word_score

def cal_sim_score(src, cand, ref_score=0):
    l = 0.5*(1.0/len(src)+1.0/len(cand))
    count = utils.lcs2(src, cand) * 1.0 + 1.05 + math.log(1.0 / (1.2 + editdistance.eval(src, cand)))

    #if src[0] == cand[0]:
    #    count += 0.1


    first_char_score,word_score=cal_matching_chars(src,cand)
    count += first_char_score + word_score
    if ref_score > 0:
        count += math.log(100.0 + ref_score) / math.log(1000)
    return count *l
```
## Thống kê một số luật thay thế từ dữ liệu

Nguyên tắc: 
B0: Sử dụng tập luật biết trước để thay thế vào dữ liệu
B1: Xác định từ sai W(rong)
B2: Thống kê bigram của các từ đứng trước từ sai B(efore) W và từ đứng sau: W A(fter)
B3: Lại thống kê bigram : các từ đứng sau của B và các từ đứng trước của A, tạo thành tập ứng cử viên đúng T(rue) cho từ sai W
B4: Xếp hạng lại các từ ứng cử viên T, sắp xếp theo khoảng cách từ, tạo ra tập luật thô
B5: Sức cơm =))


## Học không giám sát:

B0: Sử dụng các luật có được để thay thế vào dữ liệu
B1: Tạo language model cho bộ dữ liệu: Gồm xác suất xuất hiện của các từ,xác suất xuất hiện của từ sau theo từ đứng trước p(w(after)|w(before))
B2: Xác định các từ sai (theo định nghĩa của từ sai)
B3: Tìm ứng cử viên của từ sai: Duyệt theo từ điển, chọn các từ sao cho khoảng cách tới từ sai là gần nhất ( chọn top 3 từ)
B4: Tạo chuỗi markop +- 2 cho các ứng cử viên của từ sai, tính xác suất của chuỗi và chọn ứng cử viên cho xác suất lớn nhất
