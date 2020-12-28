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
