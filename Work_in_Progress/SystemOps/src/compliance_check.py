def chk_com(config_file, baseline_file):
    with open(config_file) as cf, open(baseline_file) as bf:
        config_lines = cf.readlines()
        baseline_lines = bf.readlines()

    diff = [line for line in config_lines if line not in baseline_lines]
    return diff

if __name__ == "__main__":
    result = chk_com("example_config.txt", "baseline.txt")
    if result:
        print("Non-compliant lines:", result)
    else:
        print("All lines compliant")