#!/usr/bin/env python3
import os
import re
import shlex
import subprocess
import time
from github import Github

PBANNER = "*" * 5 + " {} " + "*" * 5

class ReleaseActor():
    
    def __init__(self) -> None:
        self.github_token = self.get_env("INPUT_GITHUB_TOKEN")
        self.release_version = self.get_env("INPUT_RELEASE_VERSION")
        self.origin_branch = self.get_env("INPUT_ORIGIN_BRANCH")
        self.target_branch = self.get_env("INPUT_TARGET_BRANCH")
        self.template = self.get_env("INPUT_PR_TEMPLATE")
        self.as_draft = self.get_env("INPUT_AS_DRAFT")
        self.actor = self.get_env("GITHUB_ACTOR")
        self.repo_name = self.get_env("GITHUB_REPOSITORY")
        self.git_client = Github(self.github_token)

    def get_env(self, env_var: str):
        """Get environment variables"""
        var = os.getenv(env_var)
        if var and var.lower() == "false":
            var = False
        elif var and var.lower() == "true":
            var = True
        return var

    def run_cmd(self, cmd: str, debug: bool = True):
        """Run a shell command."""

        print(f"Running {cmd} ...")
        proc = subprocess.Popen(
            shlex.split(cmd), cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        try:
            result = proc.communicate(timeout=60)  # should configure this timeout
            std_out, std_err = result[0].decode("utf-8"), result[1].decode("utf-8")
        except subprocess.TimeoutExpired:
            print(f"{cmd} timed out, killing process and getting error.")
            proc.kill()
            std_out, std_err = proc.communicate()

        if debug:
            if std_out:
                print(PBANNER.format("stdout"))
                print(std_out)
            if std_err:
                print(PBANNER.format("stderr"))
                print(std_err)
        if proc.returncode != 0:
            raise RuntimeError(std_err)
        return std_out, std_err
    
    def run(self):
        """Open a pull request from a release branch"""
        self.run_cmd(f"git config --global user.email {self.actor}@noreply")
        self.run_cmd(f"git config --global user.name {self.actor}")

        self.run_cmd(f"git checkout {self.origin_branch}")

        if self.release_version:
            self.run_cmd(f"git checkout -b release/v{self.release_version}")
            self.run_cmd(f"npx standard-version --release-as v{self.release_version}")
        else:
            self.run_cmd("git checkout -b release/vTEMP")
            std_out = self.run_cmd("npx standard-version")
            version_list = re.findall(r'\d+', std_out[0])
            self.release_version = "{major}.{minor}.{patch}".format(
                major = version_list[0],
                minor = version_list[1],
                patch = version_list[2]
            )
            self.run_cmd(f"git branch -m release/v{self.release_version}")

        self.run_cmd(f"git push --set-upstream origin release/v{self.release_version} --follow-tags")

        repo = self.git_client.get_repo(self.repo_name)
        repo.create_pull(
            title=self.release_branch, 
            body=self.template, 
            head=self.release_branch, 
            base=self.target_branch,
            draft=self.as_draft
        )

if __name__ == "__main__":
    try:
        ReleaseActor().run()
    except Exception:
        time.sleep(1)
        raise