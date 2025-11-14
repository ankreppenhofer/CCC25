# space_pace.py
import networkx as nx
from shapely.geometry import LineString, Point
def generate_sequence(position, time_limit):
    # Determine direction
    direction = 1 if position > 0 else -1 if position < 0 else 0

    if direction == 0:
        return [0]

    # Basic sequence pattern: 0 → ±5 → ±4 → ±3 → ... → ±5 → 0
    # This pattern matches the examples
    if abs(position) < 9:
        n=abs(position)
        half_length = int(n / 2 if n % 2 == 0 else (n + 1) / 2)
        print(half_length)

        # Sequenz aufbauen (5, 4, 3, ...)
        seq_part = []
        for i in range(0,half_length):
            seq_part.append((5 - i) * direction)

        # Jetzt den vorderen Teil mit 0 beginnen
        seq = [0] + seq_part

        # Spiegel anhängen (abhängig von gerader/ungerader Position)
        if abs(n) % 2 == 0:
            seq = seq + seq[::-1]
        else:
            seq = seq + seq[-2::-1]
    else:
        num_ones = max(0, abs(position) - 8)  # Anzahl der 1er (mindestens 0)
        seq = [0, 5 * direction, 4 * direction, 3 * direction, 2 * direction] \
              + [1 * direction] * num_ones \
              + [2 * direction, 3 * direction, 4 * direction, 5 * direction, 0]

    return seq


def main():
    input_filename = "level5_0_example.in"
    output_filename = "output.txt"

    with open(input_filename, "r") as infile:
        lines = [line.strip() for line in infile if line.strip()]

    n = int(lines[0])

    with open(output_filename, "w") as outfile:
        for i in range(1, n + 1):
            pos, time_limit = lines[i].split()
            pos1,pos2 = map(int,pos.split(","))
            time_limit = int(time_limit)
            seq1= generate_sequence(pos1, time_limit)
            seq2= generate_sequence(pos2, time_limit)
            outfile.write(" ".join(map(str, seq1)) + "\n")
            outfile.write(" ".join(map(str, seq2)) + "\n")
            outfile.write("\n")

    print(f"Processed {n} cases. Results written to '{output_filename}'.")

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def shortest_path_with_obstacles(start, goal, obstacles, width, height):
    G = nx.grid_2d_graph(width, height)          # 4-Nachbarn
    G.remove_nodes_from(obstacles)               # Hindernisse entfernen
    if start not in G or goal not in G:
        return None
    return nx.astar_path(G, start, goal, heuristic=manhattan)

def expand_obstacles_square(obstacles):
    """
    Gibt alle blockierten Koordinaten im Quadrat-Radius 2 um jedes Hindernis zurück.
    Funktioniert auch mit negativen Koordinaten.
    """
    expanded = set()
    radius = 2
    for (x, y) in obstacles:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                expanded.add((x + dx, y + dy))
    return expanded

def split_into_straight_segments(path):
    if len(path) < 2:
        return [path]

    segments = []
    start = path[0]
    prev = path[0]

    # Determine initial direction
    dx_prev = path[1][0] - path[0][0]
    dy_prev = path[1][1] - path[0][1]

    for i in range(1, len(path)):
        x, y = path[i]
        dx = x - prev[0]
        dy = y - prev[1]

        # Check if direction changes
        if (dx, dy) != (dx_prev, dy_prev):
            # segment ends at previous point
            segments.append((start, prev))
            start = prev
            dx_prev, dy_prev = dx, dy

        prev = (x, y)

    # append the last segment
    segments.append((start, prev))
    return segments


def first_hit_on_line(start, goal, obstacles, hit_tolerance=0.5):
    """
    Gibt das erste Hindernis zurück, das die direkte Linie zwischen start und goal trifft.
    - start, goal: (x, y)
    - obstacles: Iterable[(x, y)]
    - hit_tolerance: wie nah ein Punkt an der Linie sein muss, Default 0.5 für Gitter

    Rückgabe:
      (ox, oy)  → erstes getroffenes Hindernis
      None      → direkter Weg ist frei
    """

    line = LineString([start, goal])
    hits = []

    for ox, oy in obstacles:
        obstacle_point = Point(ox, oy)

        # prüfe, ob der Punkt "auf" der Linie liegt
        if line.distance(obstacle_point) <= hit_tolerance:
            # gespeicherte Entfernung: wie weit entlang der Linie getroffen wurde
            dist_on_line = line.project(obstacle_point)
            hits.append((dist_on_line, (ox, oy)))

    if not hits:
        return None

    # Sortieren: das erste Hindernis auf der Linie (kleinster Abstand)
    hits.sort(key=lambda x: x[0])
    return hits[0][1]


if __name__ == "__main__":
    #main()
    # Beispiel
    start = (0, 0)
    goal = (-7, -7)
    width, height = 10, 8
    obstacles = {(-3, -3)}
    expand_obstacles_square(obstacles)

