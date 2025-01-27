#!/run/current-system/sw/bin/sh

uvicorn web_server:app --reload --host "0.0.0.0" --port 8080
