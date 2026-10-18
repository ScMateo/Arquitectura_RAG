#!/usr/bin/env bash
cd /root/mi_asistente_ia/Arquitectura_RAG/backend || exit 1
VENV=/root/mi_asistente_ia/venv/bin

pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 1

PYTHONPATH=. "$VENV/uvicorn" app.main:app --host 127.0.0.1 --port 8000 > /tmp/uvicorn.log 2>&1 &
PID=$!

READY=0
for i in $(seq 1 60); do
  if curl -s -m 2 http://127.0.0.1:8000/health > /tmp/health.out 2>/dev/null; then
    READY=1
    break
  fi
  sleep 2
done

echo "== ready after ${i}x2s: $READY =="
echo "== GET /health =="
cat /tmp/health.out 2>/dev/null; echo
echo "== GET /docs (http code) =="
curl -s -o /dev/null -w "%{http_code}\n" -m 5 http://127.0.0.1:8000/docs 2>/dev/null || echo "fail"
echo "== paths (openapi) =="
curl -s -m 5 http://127.0.0.1:8000/openapi.json 2>/dev/null | "$VENV/python" -c "import sys,json; print(list(json.load(sys.stdin)['paths'].keys()))" 2>/dev/null || echo "fail"

kill $PID 2>/dev/null || true
sleep 1
echo "== server log (tail) =="
tail -n 15 /tmp/uvicorn.log
