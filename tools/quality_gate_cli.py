import argparse
from quality_gate import evaluate

p=argparse.ArgumentParser()
p.add_argument("--build-success", action="store_true")
p.add_argument("--expect", action="append", default=[])
args=p.parse_args()

result=evaluate(args.build_success,args.expect)
print(result)
exit(0 if result["passed"] else 1)
