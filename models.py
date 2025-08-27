import datetime


class Expression:
    def __init__(self, expr: str, result: float):
        self.expr = expr
        self.result = result
        self.timestamp = datetime.now().isoformat() + "Z"
        
    