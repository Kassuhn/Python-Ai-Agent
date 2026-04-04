import os


def get_file_content(working_directory, file_path):
    try:
        
        abspath = os.path.abspath(working_directory)
        relpath = os.path.join(abspath, file_path)
        targetdir = os.path.normpath(relpath)
        commonpath = os.path.commonpath([abspath, targetdir])
        
        if commonpath != abspath:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(targetdir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(targetdir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            content = file_content_string
            
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    except Exception as e:
        return f"Error: {e}"