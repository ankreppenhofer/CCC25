# read_and_sum_modified.py
def write_sequence(space, time):
    out = ""
    if space > 0:
        if space == 1:
            out = "0 5 0"
        elif space == 2:
            out = "0 5 5 0"
        elif space == 3:
            out = "0 5 4 5 0"
        elif space == 4:
            out = "0 5 4 4 5 0"
        elif space == 5:
            out = "0 5 4 3 4 5 0"
        elif space == 6:
            out = "0 5 4 3 3 4 5 0"
        elif space == 7:
            out = "0 5 4 3 2 3 4 5 0"
        elif space == 8:
            out = "0 5 4 3 2 2 3 4 5 0"
        elif space >= 9:
            out = "0 5 4 3 2"
            for j in range(space - 8):
                out += " 1"
            out += " 2 3 4 5 0"
    else:
        if space == -1:
            out = "0 -5 0"
        elif space == -2:
            out = "0 -5 -5 0"
        elif space == -3:
            out = "0 -5 -4 -5 0"
        elif space == -4:
            out = "0 -5 -4 -4 -5 0"
        elif space == -5:
            out = "0 -5 -4 -3 -4 -5 0"
        elif space == -6:
            out = "0 -5 -4 -3 -3 -4 -5 0"
        elif space == -7:
            out = "0 -5 -4 -3 -2 -3 -4 -5 0"
        elif space == -8:
            out = "0 -5 -4 -3 -2 -2 -3 -4 -5 0"
        elif space <= -9:
            out = "0 -5 -4 -3 -2"
            for j in range(abs(space) - 8):
                out += " -1"
            out += " -2 -3 -4 -5 0"
        return out

def check (path, space, time):
    numbers = list(map(int, path.split()))

    normal_sum = sum(1 if n > 0 else -1 if n < 0 else 0 for n in numbers)

    # Modified sum (abs, but 0 counts as 1)
    modified_sum = sum(abs(n) if n != 0 else 1 for n in numbers)
    if normal_sum == space and modified_sum <= time:
        return True
    else:
        return False

def main():
    input_filename = "./level5/level5_0_example.in"
    output_filename = "./level5/output_example.out"

    with open(input_filename, "r") as infile:
        lines = [line.strip() for line in infile if line.strip()]

    num_rows = int(lines[0])

    with open(output_filename, "w") as outfile:
        out = ""

        for i in range(1, num_rows + 1):
            out = ""
            space, time = lines[i].split()
            space = int(space)
            time = int(time)
            out = write_sequence(space, time)
            print(f"{i}: space={space}, time={time} =>  Check: {check(out, space, time)}")
            if check(out, space, time) != True:
                print("Error in row ", i)
                print (f"Generated path: {out}")
            outfile.write(f"{out}\n")
    print(f"Processed {num_rows} rows. Results written to '{output_filename}'.")

main()