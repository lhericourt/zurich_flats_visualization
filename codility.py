# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):
    # write your code in Python 3.6

    # Test the cas of no value
    if len(A) == 0:
        return -1

    # Compute the mean    
    mean = sum(A) / float(len(A))

    # Compute the standard deviation for each value of the list
    list_std = [abs(x - mean) for x in A]

    # Return the index of the max
    return list_std.index(max(list_std))
