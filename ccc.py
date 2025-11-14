import os


# --- (Placeholder Functions remain the same, hidden for brevity) ---
# NOTE: Ensure your functions generatemnipulatedtournament and stillin2round are defined.
# ... (process_single_level_file function remains the same as previous response) ...
# ---------------------------------------------------------------------------------

def process_single_level_file(file_path):
    """
    Reads, processes, and writes the output for a single level input file.
    (This function is the same as the one in the previous response.)
    """
    print(f"Loading level: **{file_path}**")

    # 1. Read the input file
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return

    if not lines:
        return

    output_file_path = file_path.replace(".in", ".out")

    # 2. Parse the global parameters (N and M)
    try:
        n_str, m_str = lines[0].split()
        N = int(n_str)
        M = int(m_str)
    except (ValueError, IndexError):
        return

    out_lines = []

    # 3. Process each case from line 1 up to N cases
    # Assuming generatemnipulatedtournament and stillin2round are defined globally
    for i in range(1, N + 1):
        if i >= len(lines):
            break

        line_parts = lines[i].split()
        if len(line_parts) != 3:
            continue

        try:
            R = int(line_parts[0].rstrip("R"))
            P = int(line_parts[1].rstrip("P"))
            S = int(line_parts[2].rstrip("S"))
        except ValueError:
            continue

        # Core logic call
        # tourn = generatemnipulatedtournament(R, P, S, M)
        # out_lines.append(tourn + "\n")

        # NOTE: Using placeholders for tourn and validation to avoid errors
        # if the helper functions aren't fully defined.
        tourn = "RPS"
        out_lines.append(tourn + "\n")
        # Validation print skipped for brevity

    # 4. Write the output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

    print(f"Finished processing {len(out_lines)} cases. Output saved to **{output_file_path}**")
    print("-" * 50)


def find_and_process_all_levels(level=1,justexamples=False):
    target_files = []

    print(f"Searching for levels from {level}.")

    # 1. Check for the 'example' file
    dir_name = f"level{level}"
    example_file_name = f"level{level}_example.in"
    example_path = os.path.join(dir_name, example_file_name)

    if os.path.exists(example_path):
        target_files.append(example_path)
    if justexamples:
        if not target_files:
            print("No example level input files found (.in). Please check the directory structure.")
        else:
            print(f"\nFound **{len(target_files)}** example level files to process.")
        for file_path in target_files:
            # move example out to levelx_example_true.out
            level_example_out = "level{}_example.out".format(level)
            os.rename(os.path.join(dir_name, level_example_out), os.path.join(dir_name, level_example_out.replace(".out", "_true.out")))
            process_single_level_file(file_path)
        return
    # 2. Check for the 5 sublevels
    for sub_level in range(1, 6):  # Sublevels 1 through 5
        file_name = f"level{level}_{sub_level}.in"
        file_path = os.path.join(dir_name, file_name)

        if os.path.exists(file_path):
            target_files.append(file_path)
    if not target_files:
        print("No level input files found (.in). Please check the directory structure.")
        return
    print(f"\nFound **{len(target_files)}** level files to process.")
    # Process each found file
    for file_path in target_files:
        process_single_level_file(file_path)

if __name__ == "__main__":
    # Modify the range below if you have more or fewer main levels
    find_and_process_all_levels(1,True)
