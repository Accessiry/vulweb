# Logs Directory

This directory stores application logs.

## Log Files

- `backend.log` - Backend Flask application logs
- `frontend.log` - Frontend development server logs
- `app.log` - General application logs
- `backend.pid` - Backend process ID (when running)
- `frontend.pid` - Frontend process ID (when running)

## Log Rotation

Logs are automatically rotated when they reach 10MB.
Old logs are backed up with timestamps.

## Viewing Logs

```bash
# View backend logs
tail -f logs/backend.log

# View frontend logs
tail -f logs/frontend.log

# View last 100 lines
tail -n 100 logs/backend.log
```

## Cleaning Logs

```bash
# Remove old log files
rm logs/*.log

# Keep directory structure
find logs -type f -name "*.log" -delete
```
