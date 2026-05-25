from reconciler import reconcile_transaction_files
import sys

def main():
    if len(sys.argv) != 3:
        print('Usage: python main.py <csv1> <csv2>', file=sys.stderr)
        sys.exit(1)
    try:
        internal_path, provider_path = sys.argv[1], sys.argv[2]
        print(reconcile_transaction_files(internal_path, provider_path))
    except FileNotFoundError as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    main()
