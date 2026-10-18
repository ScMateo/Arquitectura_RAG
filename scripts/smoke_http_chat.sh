#!/usr/bin/env bash
cd /root/mi_asistente_ia/Arquitectura_RAG/backend || exit 1
VENV=/root/mi_asistente_ia/venv/bin
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 1

PYTHONPATH=. "$VENV/uvicorn" app.main:app --host 127.0.0.1 --port 8000 > /tmp/uvicorn.log 2>&1 &
PID=$!
for i in $(seq 1 60); do
  if curl -s -m 2 http://127.0.0.1:8000/health > /dev/null 2>&1; then break; fi
  sleep 2
done

echo "== POST /api/chat =="
curl -s -m 120 -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quien ha investigado sobre salud publica?", "session_id": "http1"}' \
  > /tmp/chat_resp.json

"$VENV/python" - <<'PY'
import json
d = json.load(open("/tmp/chat_resp.json"))
print("answer:", d["answer"][:300])
print("num sources:", len(d["sources"]))
if d["sources"]:
    s = d["sources"][0]
    print("first source keys:", sorted(s.keys()))
    print("first source author:", s["author"], "| url:", s["url"])
PY

kill $PID 2>/dev/null || true
sleep 1
echo "== log tail =="
tail -n 4 /tmp/uvicorn.log
