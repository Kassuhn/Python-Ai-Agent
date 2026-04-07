import os
from google.genai import types


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
        return f'Successfully wrote to "{file_path}": ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    
schema_write_files = types.FunctionDeclaration(
name="write_files",
description="Writes content to a file at the specified path relative to the working directory, creating any missing parent directories",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file to write, relative to the working directory"
,
        ),
        "content": types.Schema(
            type=types.Type.STRING,
            description="The text content to write to the file"
,
        ),
    },
    required=["file_path", "content"]
),
)