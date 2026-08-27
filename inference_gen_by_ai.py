import argparse
import os
import sys
import pickle
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference with a pickled ML model.")
    parser.add_argument(
        "--data",
        type=str,
        default="dataset/input.csv",
        help="Path to input CSV file containing data for prediction.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="model/model.pkl",
        help="Path to pickled model file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/output.csv",
        help="Path to output CSV file with predictions.",
    )
    args = parser.parse_args()

    # Check model file exists
    if not os.path.isfile(args.model):
        print(f"Error: Model file not found at '{args.model}'.", file=sys.stderr)
        sys.exit(1)

    # Check input data file exists
    if not os.path.isfile(args.data):
        print(f"Error: Input data file not found at '{args.data}'.", file=sys.stderr)
        sys.exit(1)

    # Load the model
    try:
        with open(args.model, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Error: Failed to load model from '{args.model}': {e}", file=sys.stderr)
        sys.exit(1)

    # Load input data
    try:
        df = pd.read_csv(args.data)
    except Exception as e:
        print(f"Error: Failed to read input CSV '{args.data}': {e}", file=sys.stderr)
        sys.exit(1)

    # Reject if columns contain 'target' or 'prediction'
    reserved_cols = {"target", "prediction"}
    intersect = reserved_cols.intersection(df.columns)
    if intersect:
        print(
            f"Error: Input data contains reserved column(s): {', '.join(sorted(intersect))}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Run model prediction
    try:
        preds = model.predict(df)
    except Exception as e:
        print(f"Error: Model prediction failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Prepare output DataFrame
    result_df = pd.DataFrame({"target": preds})

    # Ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir:
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            print(f"Error: Failed to create output directory '{out_dir}': {e}", file=sys.stderr)
            sys.exit(1)

    # Write predictions to output csv
    try:
        result_df.to_csv(args.output, index=False)
    except Exception as e:
        print(f"Error: Failed to write output CSV '{args.output}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
