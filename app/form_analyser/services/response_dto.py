from dataclasses import dataclass


@dataclass
class ValidationDto:
    name: str
    input: str
    parms: str
    output: str
    status: str
    message: str
