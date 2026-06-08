"""Parser for the AI Agent Employment Contract DSL."""

from .parser import Contract, ContractParseError, parse_contract

__all__ = ["Contract", "ContractParseError", "parse_contract"]
