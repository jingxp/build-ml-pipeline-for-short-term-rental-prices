#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact.
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    logger.info("Loading artifacts")
    artifact_local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    
    # Drop outliers
    logger.info(f"Drop outlier records with price between {args.min_price} and {args.max_price} dollor")
    
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # save and upload cleaned df
    logger.info("Uploading cleaned data")

    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
        )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifacts of the basic cleaning step",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output name of the basic cleaning step",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Out put file type of the basic cleaning step",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the basic cleaning step",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimun price to rule out outlier",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximun price to rule out outlier",
        required=True
    )


    args = parser.parse_args()

    go(args)
