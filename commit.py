import os
import subprocess
import getpass

def run_command(command, token=None):
    env = os.environ.copy()
    if token:
        env['GIT_ASKPASS'] = 'echo'
        env['GIT_PASSWORD'] = token
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command '{command}':")
        print(error.decode('utf-8'))
        return False
    return True

def upload_to_github(dir_path, repo_url, token):
    print(f"Changing to directory: {dir_path}")
    os.chdir(dir_path)
    
    print("Checking Git repository status...")
    if not os.path.exists('.git'):
        print("Initializing Git repository...")
        if not run_command("git init"):
            return
    else:
        print("Git repository already exists.")

    print("Creating .gitignore file...")
    with open('.gitignore', 'a') as gitignore:
        gitignore.write('\n.venv/\n')

    print("Adding files...")
    if not run_command("git add ."):
        return
    
    print("Committing changes...")
    if not run_command('git commit -m "Update commit"'):
        return
    
    print("Checking remote repository...")
    if not run_command("git remote -v"):
        return

    print("Updating remote repository...")
    if not run_command(f"git remote set-url origin {repo_url}"):
        if not run_command(f"git remote add origin {repo_url}"):
            return

    print("Creating main branch...")
    if not run_command("git branch -M main"):
        return

    print("Pulling changes from remote repository...")
    if not run_command(f"git pull --rebase origin main", token):
        print("Conflict occurred. Please resolve conflicts manually and run the script again.")
        return

    print("Pushing to GitHub...")
    if not run_command(f"git push -u origin main", token):
        return
    
    print("Directory successfully uploaded to GitHub!")

# Usage
dir_path = "/Users/griffinstrier/Virtual_Compass"
repo_url = "https://github.com/greyhatharold/Virtual_Compass.git"

# Ask for the personal access token
token = getpass.getpass("Enter your GitHub personal access token: ")

run_command("git config --global user.name 'Griffin Strier'")
run_command("git config --global user.email 'gjstrier@gmail.com'")

upload_to_github(dir_path, repo_url, token)
