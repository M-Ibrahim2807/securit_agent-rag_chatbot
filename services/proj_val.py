from pathlib import Path

def validate_project(
        repository_path:Path,
        max_python_files:int=10,
        max_loc:int=5000,
        max_size_mb:int=20,

)->None:
    python_files=list(repository_path.rglob("*.py"))
    if len(python_files)>max_python_files:
        raise Exception(
            f"project contains {len(python_files)} python files , Maximum allowed limit is {max_python_files}"

        )
    total_loc=0

    for file in python_files:
        with open(file,"r",encoding='utf-8',errors="ignore") as f:
            total_loc += sum(1 for _ in f)
        
    if total_loc > max_loc:
        raise Exception(
            f"project contains {total_loc} LOC"
            f" Max Allowed LOC {max_loc}"

        )
    
    total_size = sum(
            file.stat().st_size
            for file in repository_path.rglob("*")
            if file.is_file()
        )

    size_mb = total_size / (1024 * 1024)

    if size_mb > max_size_mb:
        raise Exception(
            f"Repository size is {size_mb:.2f} MB. "
            f"Maximum allowed is {max_size_mb} MB."
        )