import subprocess
import sys
import time
import json

# Define supported languages and their corresponding Docker images
# This matches the output of package_function.py
FUNCTION_IMAGES = {
    "python": "example_function_python",
    "javascript": "example_function_javascript"
}

def execute_function(function_name, lang, timeout=5):
    """
    Executes a function by spinning up a new container (cold start).
    """
    
    if lang not in FUNCTION_IMAGES:
        error_response = {"error": f"Unsupported language: {lang}"}
        print(json.dumps(error_response, indent=2))
        return

    image_name = FUNCTION_IMAGES[lang]
    print(f"🚀 Spawning new container for {image_name} with timeout {timeout}s...")

    try:
        # Use subprocess.run for a cleaner blocking call with a timeout
        process = subprocess.run(
            ["docker", "run", "--rm", image_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True
        )

        # Get output
        output = process.stdout
        error = process.stderr
        return_code = process.returncode

        response = {
            "function": function_name,
            "language": lang,
            "timeout": timeout,
            "status": "success" if return_code == 0 else "failed",
            "output": output.strip() if output else None,
            "error": error.strip() if error else None
        }

    except subprocess.TimeoutExpired:
        print(f"⏳ Timeout exceeded! Function {function_name} took longer than {timeout} seconds.")
        response = {
            "function": function_name,
            "language": lang,
            "timeout": timeout,
            "status": "failed",
            "output": None,
            "error": f"Function exceeded timeout of {timeout} seconds."
        }

    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python execute_function.py <function_name> <language> [timeout]")
        sys.exit(1)

    function_name = sys.argv[1]
    lang = sys.argv[2]
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 5  # Default timeout: 5 seconds

    execute_function(function_name, lang, timeout)