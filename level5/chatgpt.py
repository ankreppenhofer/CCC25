# generate_2d_sequences_with_asteroids.py
import networkx as nx

def expand_obstacles_square(obstacles, radius=2):
    expanded = set()
    for (x, y) in obstacles:
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                expanded.add((x+dx, y+dy))
    return expanded

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def build_graph_covering(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    G = nx.grid_2d_graph(w, h)
    mapping = { (i, j): (i + min_x, j + min_y) for i in range(w) for j in range(h)}
    G = nx.relabel_nodes(G, mapping)
    return G

def shortest_path_with_obstacles(start, goal, obstacles):
    points = [start, goal] + list(obstacles)
    G = build_graph_covering(points)
    G.remove_nodes_from(obstacles)
    if start not in G or goal not in G:
        return None
    try:
        return nx.astar_path(G, start, goal, heuristic=manhattan)
    except nx.NetworkXNoPath:
        return None

def split_into_straight_segments(path):
    if not path or len(path) < 2:
        return [(path[0], path[0])] if path else []
    segments = []
    start = path[0]
    prev = path[0]
    dx_prev = path[1][0] - path[0][0]
    dy_prev = path[1][1] - path[0][1]
    for i in range(1, len(path)):
        x, y = path[i]
        dx = x - prev[0]
        dy = y - prev[1]
        if (dx, dy) != (dx_prev, dy_prev):
            segments.append((start, prev))
            start = prev
            dx_prev, dy_prev = dx, dy
        prev = (x, y)
    segments.append((start, prev))
    return segments

def gen_1d_from_displacement(n):
    if n == 0:
        return [0]
    sign = 1 if n > 0 else -1
    a = abs(n)
    if a == 1:
        seq = [0,5,0]
    elif a == 2:
        seq = [0,5,5,0]
    elif a == 3:
        seq = [0,5,4,5,0]
    elif a == 4:
        seq = [0,5,4,4,5,0]
    elif a == 5:
        seq = [0,5,4,3,4,5,0]
    elif a == 6:
        seq = [0,5,4,3,3,4,5,0]
    elif a == 7:
        seq = [0,5,4,3,2,3,4,5,0]
    elif a == 8:
        seq = [0,5,4,3,2,2,3,4,5,0]
    else:
        ones = a-8
        seq = [0,5,4,3,2] + [1]*ones + [2,3,4,5,0]
    return [v*sign for v in seq]

def build_2d_sequences_from_path(path):
    seq_x = []
    seq_y = []
    segments = split_into_straight_segments(path)
    for (start, end) in segments:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx != 0 and dy == 0:
            s = gen_1d_from_displacement(dx)
            seq_x.extend(s)
            seq_y.extend([0]*len(s))
        elif dy != 0 and dx == 0:
            s = gen_1d_from_displacement(dy)
            seq_y.extend(s)
            seq_x.extend([0]*len(s))
    return seq_x, seq_y

def format_seq(seq):
    return " ".join(str(x) for x in seq)

def main(input_filename="level5_0_example.in", output_filename="output_example.out"):
    with open(input_filename,"r") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    T = int(lines[0])
    idx = 1
    outputs = []
    for case in range(T):
        goal_line = lines[idx]; idx += 1
        asteroid_line = lines[idx]; idx += 1
        gx, gy = map(int, goal_line.split()[0].split(","))
        time_limit = int(goal_line.split()[1])
        ax, ay = map(int, asteroid_line.split(","))
        obstacles = {(ax, ay)}
        start = (0,0)  # falls Start nicht gegeben, sonst anpassen
        blocked = expand_obstacles_square(obstacles, radius=2)
        path = shortest_path_with_obstacles(start, (gx, gy), blocked)
        if path is None:
            # fallback: direkter L-Pfad
            path = [start]
            x, y = start
            step = 1 if gx > x else -1
            while x != gx:
                x += step
                path.append((x,y))
            step = 1 if gy > y else -1
            while y != gy:
                y += step
                path.append((x,y))
        seq_x, seq_y = build_2d_sequences_from_path(path)
        outputs.append(format_seq(seq_x))
        outputs.append(format_seq(seq_y))
        outputs.append("")
    with open(output_filename,"w") as out:
        out.write("\n".join(outputs))
    print(f"Wrote {T} cases to {output_filename}")

if __name__=="__main__":
    main()
