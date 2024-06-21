import subprocess

def run_script_and_capture_logs(script_path):
    # Attempt to run the script using subprocess
    try:
        # Open a process to run the Python script
        process = subprocess.Popen(
            ['python', script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Collect output and error messages
        stdout, stderr = process.communicate()

        # Check for errors in execution
        if process.returncode != 0:
            print(f"Error occurred while executing the script: {stderr}")
        else:
            print("Script executed successfully. Output:")
            print(stdout)


        return stdout, stderr

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the script: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

# Path to the script you want to run
script_path = 'D:/Stage Air 2024/spring/python-server/AutoExtract+Behavior/part2.py'

# Run the function with the path to your script
run_script_and_capture_logs(script_path)
