from log_analyzer import analyze_log_file
import sys

def main():
    if len(sys.argv) != 2:
        print('Error: requires 2 arguments')
        sys.exit(1)
    try:
        filepath = sys.argv[1]
        analyzedLogFile = analyze_log_file(filepath)
        print(analyzedLogFile)
    except FileNotFoundError as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
