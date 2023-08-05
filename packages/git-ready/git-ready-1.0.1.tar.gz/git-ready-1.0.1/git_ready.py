# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Get ready to commit."""

import argparse
import subprocess
import sys


MASTER = 'master'


def ensure_remote_branch_is_tracked(branch):
    """Track the specified remote branch if it is not already tracked."""
    if branch == MASTER:
        # We don't need to explicitly track the master branch, so we're done.
        return

    # Ensure the specified branch is in the local branch list.
    output = subprocess.check_output(['git', 'branch', '--list'])
    for line in output.split('\n'):
        if line.strip() == branch:
            # We are already tracking the remote branch
            break
    else:
        # We are not tracking the remote branch, so track it.
        sys.stdout.write(subprocess.check_output(
            ['git', 'checkout', '--track', 'origin/%s' % branch]))


def main(branch):
    """Checkout, update and branch from the specified branch."""
    try:
        # Ensure that we're in a git repository. This command is silent unless
        # you're not actually in a git repository, in which case, you receive a
        # "Not a git repository" error message.
        sys.stdout.write(subprocess.check_output(['git', 'rev-parse']))
    except subprocess.CalledProcessError:
        # Bail if we're not in a git repository.
        return

    # This behavior ensures a better user experience for those that aren't
    # intimately familiar with git.
    ensure_remote_branch_is_tracked(branch)

    # Switch to the specified branch and update it.
    subprocess.check_call(['git', 'checkout', '--quiet', branch])

    # Pulling is always safe here, because we never commit to this branch.
    subprocess.check_call(['git', 'pull', '--quiet'])

    # Checkout the top commit in the branch, effectively going "untracked."
    subprocess.check_call(['git', 'checkout', '--quiet', '%s~0' % branch])

    # Clean up the repository of Python cruft. Because we've just switched
    # branches and compiled Python files should not be version controlled,
    # there are likely leftover compiled Python files sitting on disk which may
    # confuse some tools, such as sqlalchemy-migrate.
    subprocess.check_call(['find', '.', '-name', '"*.pyc"', '-delete'])

    # For the sake of user experience, give some familiar output.
    print('Your branch is up to date with branch \'origin/%s\'.' % branch)


def cli():
    parser = argparse.ArgumentParser(
        description='Get ready to commit, socially.')
    parser.add_argument(
        'branch', nargs='?', default=MASTER,
        help='The branch to work from.')

    args = parser.parse_args()

    try:
        main(args.branch)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    cli()
