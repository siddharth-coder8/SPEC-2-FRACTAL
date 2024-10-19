import os
import sys
from huggingface_hub import login

# Authenticate to Hugging Face (replace with your actual token)
login(token="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")

# Setting up the root directory and adding it to system path
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

try:
    # Import pygit2 and configure
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    # Open the current repository
    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    # Get the current branch name
    branch_name = repo.head.shorthand

    # Define the remote name and fetch from it
    remote_name = 'origin'
    remote = repo.remotes[remote_name]

    remote.fetch()

    # Define local and remote references
    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    # Check if the repository is up-to-date
    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        # Perform a fast-forward merge
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge completed successfully.")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Possible local modifications exist. Manual intervention may be required.")
except Exception as e:
    print('Update failed due to an error.')
    print(str(e))

print('Update check completed.')

# Import additional functions from the launch module
from launch import *