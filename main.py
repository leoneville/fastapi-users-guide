import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'fastapi_users_guide.app:app', 
        host='0.0.0.0', 
        log_level='info', 
        reload=True,
    )