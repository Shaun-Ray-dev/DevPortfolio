import os

def chk_com(config_file, baseline_file):
    with open(config_file) as cf, open(baseline_file) as bf:
        config_lines = cf.readlines()
        baseline_lines = bf.readlines()

    diff = [line for line in config_lines if line not in baseline_lines]
    return diff

if __name__ == "__main__":
    SRC_DIR = os.path.dirname(__file__)
    config_file = os.path.join(SRC_DIR, "example_config.txt")
    baseline_file = os.path.join(SRC_DIR, "baseline_config.txt")
    
    result = chk_com(config_file, baseline_file)
    
    if result:
        print("Non-compliant lines:", result)
    else:
        print("All lines compliant")
