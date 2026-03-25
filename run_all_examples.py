# run_all_examples.py

import subprocess
import sys
import glob
import os
from concurrent.futures import ThreadPoolExecutor 
from typing import Dict, Any

def run_single_example(filepath: str, python_executable: str) -> Dict[str, Any]:
    """执行单个示例脚本，并捕获其输出和状态。"""
    filename = os.path.basename(filepath)
    try:
        # We use subprocess.run to execute the script in a separate process.
        # This is important because each script might modify matplotlib's state,
        # and running them in separate processes ensures they don't interfere
        # with each other.
        result = subprocess.run(
            [python_executable, filepath],
            capture_output=True, text=True, check=True, encoding='utf-8', errors='replace'
        )
        return {
            'filename': filename,
            'status': 'success',
            'stdout': result.stdout,
            'stderr': '' # stderr is empty on success with check=True
        }
    except subprocess.CalledProcessError as e:
        return {
            'filename': filename,
            'status': 'error',
            'stdout': e.stdout,
            'stderr': e.stderr,
            'returncode': e.returncode
        }
    except Exception as e:
        return {
            'filename': filename,
            'status': 'unexpected_error',
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def run_examples():
    """Finds and runs all Python example scripts in the 'examples' directory
    and its subdirectories using a thread pool for parallel execution, while
    ensuring results are collected and printed in submission order."""
    # Get the path to the current python interpreter
    python_executable = sys.executable
    
    # Get the root directory of the script
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all example files
    example_files = glob.glob(os.path.join(root_dir, 'examples', '**', '*.py'), recursive=True)
    
    if not example_files:
        print("No example files found.")
        return

    print(f"Found {len(example_files)} example files to run in parallel.")
    print("-" * 50)

    results = []
    # 使用 with 语句可以确保线程池被正确关闭
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        # 提交所有任务，并保持 future 对象的顺序
        futures_in_order = [executor.submit(run_single_example, fp, python_executable) for fp in example_files]

        # 按提交顺序等待结果
        for future in futures_in_order:
            results.append(future.result())

    # --- 所有任务已经并发执行完毕，现在按顺序打印结果 ---

    for i, res in enumerate(results):
        filename = res['filename']
        print(f"[{i+1}/{len(results)}] Result for: {filename}")

        if res['status'] == 'success':
            if res['stdout']:
                print(res['stdout'])
        elif res['status'] == 'error':
            print(f"--- ERROR in {filename} ---")
            print(f"Return Code: {res['returncode']}")
            if res['stdout']:
                print("--- STDOUT ---")
                print(res['stdout'])
            if res['stderr']:
                print("--- STDERR ---")
                print(res['stderr'])
        elif res['status'] == 'unexpected_error':
            print(f"An unexpected error occurred while trying to run {filename}: {res['stderr']}")

        print("-" * 50)

if __name__ == "__main__":
    run_examples()
