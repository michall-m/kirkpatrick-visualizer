def det(p,q,r):
   return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


def orientation(p, q, r, epsilon = 0):
        d = det(p,q,r)
        if d > epsilon:
            return 1 #"clockwise" #lewa
        elif d < (-1)*epsilon:
            return -1 #"counterclockwise" #prawa
        else:
            return 0 #"collinear"


def compareKey1(key):
    return key.point.y


def compareKey2(key):
    return key[0].point.y


def binary_searchleftmost(arr, val, left, right):
    if left==right:
        if arr[left][0].point.y == val:
            return left
        else:
            return -1
    (mid) = (int)((left+right)/2)
    if arr[mid][0].point.y < val:
        return binary_searchleftmost(arr, val, mid+1, right)
    else:
        return binary_searchleftmost(arr, val, left, mid)
