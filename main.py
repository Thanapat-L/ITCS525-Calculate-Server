import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from models import Expression,CalculatorLog

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        expr = expr.replace('÷','/').replace('×','*')
        code = Expression(expr=expr).expand_percent()
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        history.appendleft(CalculatorLog(expr=Expression(expr=expr).expr, result=float(result)))
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}


@app.get("/history", response_model=list[CalculatorLog])
def get_history(limit: int = 50):
    return list(history)[: max(0, min(limit, HISTORY_MAX))]

@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "cleared": True}