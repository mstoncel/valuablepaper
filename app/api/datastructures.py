from dataclasses import dataclass


@dataclass
class ResponsePayload:
    error: bool
    results: list

@dataclass
class ResponseError:
    error: bool
