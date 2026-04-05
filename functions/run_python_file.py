import os
import subprocess


def run_python_file(working_directory, file_path, args=None):

    try:
        
        abspath = os.path.abspath(working_directory)
        relpath = os.path.join(abspath, file_path)
        targetdir = os.path.normpath(relpath)
        commonpath = os.path.commonpath([abspath, targetdir])
        
        if commonpath != abspath:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(targetdir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", targetdir]
        command.extend(args or [])
        cmdout = subprocess.run(command,
                                cwd=abspath,
                                capture_output=True,
                                text=True,
                                timeout=30
                                )
        
        output = ""
        
        if cmdout.returncode != 0:
            output += f"Process exited with code {cmdout.returncode}\n"
        if not cmdout.stdout and not cmdout.stderr:
            output += "No output produced"

        else:
            if cmdout.stdout:
                output += f"STDOUT:\n{cmdout.stdout}"
            if cmdout.stderr:
                output += f"STDERR:\n{cmdout.stderr}"
            if not output:
                output = "No output produced"
        return output



    except Exception as e:
        return f"Error: executing Python file: {e}"