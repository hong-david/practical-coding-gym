from log_analyzer import analyze_log_file
import sys

def main():
  if len(sys.argv) != 2:
    print("Usage: python main.py <log-file>", file=sys.stderr)
    sys.exit(1)
  filepath = sys.argv[1]
  try:
    result = analyze_log_file(filepath)
    print(result)
  except FileNotFoundError:
    print(f"Error: file not found: {filepath}", file=sys.stderr)
    sys.exit(1)
if __name__ == "__main__":
    main()
