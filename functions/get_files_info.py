import os


def get_files_info(working_directory, directory="."):
    try:
        
        abspath = os.path.abspath(working_directory)
        relpath = os.path.join(abspath, directory)
        targetdir = os.path.normpath(relpath)
        commonpath = os.path.commonpath([abspath, targetdir])
        
        if commonpath != abspath:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(targetdir):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for item in os.listdir(targetdir):
            item_path = os.path.join(targetdir, item)
            size = os.path.getsize(item_path)
            isdir = os.path.isdir(item_path)
            lines.append(f"- {item}: file size={size} bytes, is_dir={isdir}")
        
        if directory == ".":
            return "Result for current directory:\n" + "\n".join(lines)
        else:
            return f"Result for {directory} directory:\n" + "\n".join(lines)
    
    except Exception as e:
        return f"Error: {e}"