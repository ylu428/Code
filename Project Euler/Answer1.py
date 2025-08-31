'''
Multiples of 3 or 5
Problem 1
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. 
The sum of these multiples is 23.
Find the sum of all the multiples of 3 or 5 below 1000.
'''

def func(below, multipler):
    q, r = divmod(below, multipler)
    result = sum([multipler*(i+1) for i in range(q if r!=0 else q-1)])
    return result

ans = func(1000,3)+func(1000,5)-func(1000,15)
print(ans)

# Ans = 233168