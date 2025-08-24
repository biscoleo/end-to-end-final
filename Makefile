# Global
BACKEND_IMAGE=toxicity-api
FRONTEND_IMAGE=toxicity-ui
MONITOR_IMAGE=toxicity-monitor

BACKEND_CONTAINER=toxicity-api-container
FRONTEND_CONTAINER=toxicity-ui-container
MONITOR_CONTAINER=toxicity-monitor-container

BACKEND_PORT=8000
FRONTEND_PORT=8501
MONITOR_PORT=8602

# --- Backend ---
build-backend:
	docker build -t $(BACKEND_IMAGE) ./backend

run-backend:
	docker run -d --name $(BACKEND_CONTAINER) -p $(BACKEND_PORT):8000 --env-file ./backend/.env $(BACKEND_IMAGE)

stop-backend:
	-docker stop $(BACKEND_CONTAINER)
	-docker rm $(BACKEND_CONTAINER)

logs-backend:
	docker logs -f $(BACKEND_CONTAINER)

test-backend:
	curl --fail http://127.0.0.1:$(BACKEND_PORT)/health

# --- Frontend ---
build-frontend:
	docker build -t $(FRONTEND_IMAGE) ./frontend

run-frontend:
	docker run -d --name $(FRONTEND_CONTAINER) -p $(FRONTEND_PORT):8501 $(FRONTEND_IMAGE)

stop-frontend:
	-docker stop $(FRONTEND_CONTAINER)
	-docker rm $(FRONTEND_CONTAINER)

logs-frontend:
	docker logs -f $(FRONTEND_CONTAINER)

# --- Monitoring ---
build-monitor:
	docker build -t $(MONITOR_IMAGE) ./monitoring

run-monitor:
	docker run -d --name $(MONITOR_CONTAINER) -p $(MONITOR_PORT):8502 --env-file ./backend/.env $(MONITOR_IMAGE)

stop-monitor:
	-docker stop $(MONITOR_CONTAINER)
	-docker rm $(MONITOR_CONTAINER)

logs-monitor:
	docker logs -f $(MONITOR_CONTAINER)

# --- Combo Commands ---
rebuild-all: stop-all build-backend build-frontend build-monitor

run-all: run-backend run-frontend run-monitor

stop-all: stop-backend stop-frontend stop-monitor
