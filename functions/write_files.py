import os

def write_file(working_directory, file_path, content):
    try:
        
        abspath = os.path.abspath(working_directory)
        relpath = os.path.join(abspath, file_path)
        targetdir = os.path.normpath(relpath)
        commonpath = os.path.commonpath([abspath, targetdir])
        
        if commonpath != abspath:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(targetdir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(targetdir), exist_ok=True)
        
        with open(targetdir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}: {len(content)} characters written"'

    except Exception as e:
        return f"Error: {e}"