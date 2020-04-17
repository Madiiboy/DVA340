def find_it(seq):
    empty = {}
    for s in seq:
        empty[s] = 0
    for s in seq:
        empty[s] += 1
    for e in empty:
        if empty[e] > 2:
            return e

if __name__ == "__main__":
   print(find_it([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5]))