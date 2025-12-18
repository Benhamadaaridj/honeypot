def analyze_logs(file_path="logs/attacks.log"):
    
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    print(f"Total attempts: {len(lines)}")
    for line in lines[-5:]:  
        print(line.strip())
