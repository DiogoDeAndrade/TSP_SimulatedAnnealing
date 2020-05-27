import random

distances = {
    ("Lisboa", "Aveiro") : 255,
    ("Lisboa", "Castelo Branco") : 224,
    ("Lisboa", "Beja") : 178,
    ("Lisboa", "Vilamoura") : 263,

    ("Aveiro", "Lisboa") : 255,
    ("Aveiro", "Castelo Branco") : 200,
    ("Aveiro", "Beja") : 389,
    ("Aveiro", "Vilamoura") : 475,

    ("Castelo Branco", "Aveiro") : 200,
    ("Castelo Branco", "Lisboa") : 224,
    ("Castelo Branco", "Beja") : 275,

    ("Beja", "Lisboa") : 178,
    ("Beja", "Castelo Branco") : 275,
    ("Beja", "Aveiro") : 389,
    ("Beja", "Vilamoura") : 130,

    ("Vilamoura", "Lisboa") : 263,
    ("Vilamoura", "Aveiro") : 475,
    ("Vilamoura", "Beja") : 130,
}

def GetCitiesFromDistances():
    global distances

    ret = []
    for c in distances.keys():
        if (not c[0] in ret):
            ret.append(c[0])

    return ret

def GetPathLen(path):
    global distances
    l = 0
    for i in range(len(path) - 1):
        d = (path[i], path[i+1])
        if (d in distances):
            l += distances[d]
        else:
            return -1
    
    return l

def BuildInitialPath(start):
    global cities

    while (True):
        c = cities[:]
        c.remove(start)
        ret = [ start ]
        while (len(c) > 0):
            cc = random.choice(c)
            c.remove(cc)
            ret.append(cc)
        
        ret.append(start)

        path_len = GetPathLen(ret)

        if (path_len > 0):
            return ret, path_len

def IsEqual(s1, s2):
    for idx, c in enumerate(s1):
        if (c != s2[idx]):
            return False
    
    return True

def AlreadyVisited(seq):
    global saved_paths

    for n in saved_paths:
        if (IsEqual(n[0], seq)):
            return True

    return False

start = "Lisboa"
cities = GetCitiesFromDistances()

T = 0.5
alpha = 0.01
max_iters = T/alpha

initial_path, initial_length = BuildInitialPath(start)

saved_paths = []
head = initial_path
current_l = initial_length
n_cities = len(cities)

saved_paths.append((head, current_l))

iters = 0

while (True):
    p1 = random.randint(1, n_cities - 1)
    p2 = random.randint(1, n_cities - 1)
    if (p1 == p2):
        continue

    new_head = head[:]
    tmp = new_head[p1]
    new_head[p1] = new_head[p2]
    new_head[p2] = tmp

    l = GetPathLen(new_head)
    if (l == -1):
        # Invalid path, retry
        continue

    b = False
    r = random.uniform(0.0, 1.0)
    if (r <= T):
        if (l > current_l):
            head = new_head
            current_l = l
            b = True
    else:
        if (l < current_l):
            head = new_head
            current_l = l
            b = True

    if (b):
        if (not AlreadyVisited(head)):
            saved_paths.append((head, current_l))
    else:
        if (T <= 0):
            break

    T = T - alpha
    iters += 1

saved_paths = sorted(saved_paths, key=lambda tup: tup[1])

print(f"Solution found in {iters} iterations (predicted {max_iters})")
print(saved_paths[0])
