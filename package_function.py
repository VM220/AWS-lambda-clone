import os
import subprocess

# Define base images
BASE_IMAGES = {
    "python": "serverless-python",
    "javascript": "serverless-javascript"
}

# Function to package a user-defined function
def package_function(lang, function_name):
    # Validate language
    if lang not in BASE_IMAGES:
        print(f"Error: Unsupported language '{lang}'. Choose 'python' or 'javascript'.")
        return
    
    # --- THIS IS THE FIX ---
    # We change 'python' to 'py'
    file_extension = 'py' if lang == 'python' else 'js'
    
    # Define paths
    function_dir = f"function/{lang}/{function_name}"
    dockerfile_path = f"{function_dir}/Dockerfile"
    function_file = f"{function_dir}/{function_name}.{file_extension}"

    # Create function directory if not exists
    os.makedirs(function_dir, exist_ok=True)

    # Ensure function file exists
    with open(function_file, "w") as f:
        f.write(f'console.log("Hello from {function_name}!");' if lang == "javascript" else f'print("Hello from {function_name}!")')

    # Generate a function-specific Dockerfile
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(f"""\
FROM {BASE_IMAGES[lang]}
WORKDIR /app
COPY {function_name}.{file_extension} .
CMD { '["python3", "' + function_name + '.py"]' if lang == 'python' else '["node", "' + function_name + '.js"]' }
""")

    # Build the Docker image
    image_name = f"{function_name}_{lang}"
    print(f"📦 Building Docker image: {image_name} ...")
    
    # We add --no-cache to force Docker to build fresh
    subprocess.run(["docker", "build", "--no-cache", "-t", image_name, "-f", dockerfile_path, function_dir])

    print(f"✅ Function '{function_name}' is packaged as {image_name}.")

# Example usage
if __name__ == "__main__":
    package_function("python", "example_function")
    package_function("javascript", "example_function")