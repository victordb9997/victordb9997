from __future__ import annotations

import argparse
import json
import sys

from .parser import ContractParseError, parse_contract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse an AI agent employment contract DSL file.")
    parser.add_argument("contract_file", help="Path to a .contract file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args(argv)

    try:
        with open(args.contract_file, encoding="utf-8") as handle:
            contract = parse_contract(handle.read())
    except OSError as exc:
        print(f"could not read contract: {exc}", file=sys.stderr)
        return 2
    except ContractParseError as exc:
        print(f"invalid contract: {exc}", file=sys.stderr)
        return 1

    indent = 2 if args.pretty else None
    print(json.dumps(contract.to_dict(), indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
