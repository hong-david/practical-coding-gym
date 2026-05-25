from log_analyzer import analyze_log_file
import sys

def main():
    if len(sys.argv) != 2:
        print('Usage: python problems/001-log-analyzer/src/main.py <log-file>', file=sys.stderr)
        sys.exit(1)
    try:
        filepath = sys.argv[1]
        summary = analyze_log_file(filepath)
        print(summary)
    except FileNotFoundError as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
