import argparse
from pipeline import Pipeline

parser=argparse.ArgumentParser()
parser.add_argument("--preview",action="store_true")
parser.add_argument("--apply",action="store_true")
args=parser.parse_args()

if args.preview:
    print("Preview mode")
Pipeline().run()
if args.apply:
    print("Apply mode (future implementation)")
