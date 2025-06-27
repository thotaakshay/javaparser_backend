import subprocess

def extract_method(java_file):
    # On Windows, use ';' in classpath. On Mac/Linux, use ':'
    cmd = [
        'java', '-cp', '.:javaparser-core-3.25.4.jar',
        'ExtractMethod', java_file
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print("Error:", result.stderr)
        return None
    return result.stdout.strip()

if __name__ == "__main__":
    # Test with your sample file
    output = extract_method('HelloWorld.java')
    print("Extracted method:\n", output)

