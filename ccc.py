# read_and_sum_modified.py

def main():
    input_filename = "./level3/level3_2_large.in"
    output_filename = "./level3/output_.out"

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
            if space > 0 :
                if space == 1:
                    out = "0 5 0"
                if space == 2:
                    out = "0 5 5 0"
                if space == 3:
                    out = "0 5 4 5 0"
                if space == 4:
                    out = "0 5 4 4 5 0"
                if space == 5:
                    out = "0 5 4 3 4 5 0"
                if space == 6:
                    out = "0 5 4 3 3 4 5 0"
                if space == 7:
                    out = "0 5 4 3 2 3 4 5 0"
                if space == 8:
                    out = "0 5 4 3 2 2 3 4 5 0"
                if space > 9:
                    out = "0 5 4 3 2"
                    for j in range(space-8):
                        out += " 1"
                    out += " 2 3 4 5 0"
            else:
                if space == -1:
                    out = "0 -5 0"
                if space == -2:
                    out = "0 -5 -5 0"
                if space == -3:
                    out = "0 -5 -4 -5 0"
                if space == -4:
                    out = "0 -5 -4 -4 -5 0"
                if space == -5:
                    out = "0 -5 -4 -3 -4 -5 0"
                if space == -6:
                    out = "0 -5 -4 -3 -3 -4 -5 0"
                if space == -7:
                    out = "0 -5 -4 -3 -2 -3 -4 -5 0"
                if space == -8:
                    out = "0 -5 -4 -3 -2 -2 -3 -4 -5 0"
                if space < -9:
                    out = "0 -5 -4 -3 -2"
                    for j in range(abs(space) - 8):
                        out += " -1"
                    out += " -2 -3 -4 -5 0"
            outfile.write(f"{out}\n")
    print(f"Processed {num_rows} rows. Results written to '{output_filename}'.")

main()