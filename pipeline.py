"""
Data Processing Pipeline
DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""
import argparse
import logging
import sys
from pprint import pprint

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data processing pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", "-c", required=True,
                        help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments parsed: input=%s, config=%s, output=%s",
                 args.input, args.config, args.output)

    # Validate input and config files
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load data and configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # Validate the DataFrame
    rows_loaded = len(data)
    try:
        df = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows", rows_loaded, len(df))

    # Process
    df_before = df.copy()
    try:
        df_after = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_before, df_after)
    logger.info("Processing complete: %d -> %d rows", len(df_before), len(df_after))

    # Save
    output_path = save_data(df_after, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    # Print the cleaning report at the end
    print("Cleaning report:")
    pprint(report)


if __name__ == "__main__":
    main()