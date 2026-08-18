from pathlib import Path


ignore_directories={
    ".git",
        "__pycache__",
        "venv",
        ".venv",
        "env",
        "node_modules",
        "dist",
        "build",
}

def read_python_files(repository_path:Path):
    files=[]
    
    for file in repository_path.rglob("*.py"):
        flag=False
        for parts in file.parts:
            if parts in ignore_directories:
                flag=True
                break
        if flag==True:
            continue

        with open(file,"r",encoding="utf-8",errors="ignore") as f :
            files.append(
                {
                "file_name":file.name,
                "relative_path":str(file.relative_to(repository_path)),
                "absolute_path":str(file),
                "source_code":f.read(),
                }

            )
    return files


                  