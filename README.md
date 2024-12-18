## Eco-Footprint 백엔드 서버

### Note

- 백엔드 서버 배포 자동화

  ```bash
  #!/bin/bash

  # uvicorn command to run the FastAPI app
  UVICORN_CMD="uvicorn main:app --reload --host 0.0.0.0 --port 80"

  LOG_DIR='log'
  if [ ! -d "$LOG_DIR" ]; then
      mkdir $LOG_DIR
  fi

  # Help message
  # Option: --help, -H
  if [ "$1" == "--help" ] || [ "$1" == "-H" ]; then
      echo "Usage: ./server.sh [OPTIONS]"
      echo "Options:"
      echo "  --background, -B  Run the FastAPI app in the background"
      echo "  --kill, -K        Kill the running FastAPI app"
      exit 0
  fi

  # Run the uvicorn command in the background
  # Option: --background, -B
  if [ "$1" == "--background" ] || [ "$1" == "-B" ]; then
      nohup $UVICORN_CMD > "$LOG_DIR/uvicorn_$(date +"%Y%m%d_%H%M%S").log" 2>&1 &
      echo "FastAPI app is running in the background"
      exit 0
  fi

  # Kill the existing FastAPI app
  # Option: --kill, -K
  if [ "$1" == "--kill" ] || [ "$1" == "-K" ]; then
      PID=$(pgrep -f "uvicorn main:app")
      if [ -z "$PID" ]; then
          echo "FastAPI app is not running"
      else
          kill $PID
          echo "FastAPI app is killed"
      fi
      exit 0
  fi

  # Run the uvicorn command in the foreground
  $UVICORN_CMD

  ```
