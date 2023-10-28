import argparse
import os
import subprocess
import time


def get_args():
    parser = argparse.ArgumentParser(
        description="A File Watcher that executes the specified tests"
    )
    parser.add_argument('--tests', action='store', required=True,
                        help='The path to the test file to run')
    parser.add_argument('--project', action='store', required=False,
                        help='The folder where the project files are')
    return parser.parse_args()


def watcher(test_path, project_path=None):
    if not project_path:
        project_path = os.path.dirname(test_path)
    f_dict = {}
    while True:
        files = os.listdir(project_path)
        for f in files:
            full_path = os.path.join(project_path, f)
            mod_time = os.stat(full_path).st_mtime
            if full_path not in f_dict:
                f_dict[full_path] = mod_time
            elif mod_time != f_dict[full_path] and f != "__pycache__":
                # Run the tests
                cmd = ['python', test_path]
                subprocess.call(cmd)
                print('-' * 70)
                f_dict[full_path] = mod_time
        time.sleep(1)


def main():
    args = get_args()
    w = watcher(args.tests, args.project)


if __name__ == '__main__':
    main()
