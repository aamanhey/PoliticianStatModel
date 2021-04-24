
# P(A and B) = P(A)P(B|A)

def prob_a_given_b(a, b, total):
    #P(a and b)
    pb = b/total
    pa = a/total
    pab = pa * pb
    pagb = pab / pb
    return pagb

MM = 287
MW = 57
WM = 40
WW = 15

'''
We want to know the probability of a candidate winning given they are a woman,
P(winning|woman) = P(winning AND woman) / P(woman)

P(winning AND woman) = (WM + WW) / total races
P(woman) = probability of being a woman = (MW + WM + WW) / total races
'''
total = MM + MW + WM + WW

Pof_winANDwoman = (WM + WW) / total
Pof_woman = (MW + WM + WW) / total
Pof_winGwoman = Pof_winANDwoman / Pof_woman

print("P(winning AND woman)",Pof_winANDwoman)
print("P(woman)", Pof_woman)
print("P(winning|woman)", Pof_winGwoman)
