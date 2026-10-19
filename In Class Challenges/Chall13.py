

def a1(nums):
    d1 = 0
    for n in nums:
        d1 += n
        n + 1
    return d1

def a2(nums):
    d1 = a1(nums)
    d2 = 0
    for n in nums:
        d2 += 1
        n + 1
    return (d1 / d2)

def a3(nums):
    d1 = 0
    for n in nums:
        if (n % 2) != 0:
            d1 += 1
    return d1

def a4(nums):
    d1 = 0
    d2 = 0
    for n in nums:
        if (n % 2) != 0:
            if d2 == 1:
                d1 += 1
            d2 = 1
        if (n % 2) == 0:
            d2 = 0
    return d1
        
numSet = [4, 2, 16, 5, 19, 5, 6, 2, 3, 5, 15, 4, 6, 10, 13, 1, 18, 6, 9, 10, 9,
12, 6, 9, 11, 18, 16, 18, 4, 9, 15, 7, 20, 12, 1, 4, 20, 17, 6, 12, 20,
19, 13, 10, 10, 7, 8, 2, 18, 20, 1, 7, 17, 3, 8, 10, 7, 1, 15, 7, 3, 13,
14, 12, 19, 13, 7, 17, 2, 14, 3, 17, 5, 12, 16, 6, 10, 15, 8, 2, 7, 1,
18, 16, 17, 12, 7, 14, 10, 17, 12, 19, 2, 20, 16, 7, 20, 16, 5, 7]

def main():
    d1 = a1(numSet)
    d2 = a2(numSet)
    d3 = a3(numSet)
    d4 = a4(numSet)
    d5 = (a1(numSet) + a2(numSet) + a3(numSet) + a4(numSet))
    print(d5)

if __name__ == "__main__":
    main()