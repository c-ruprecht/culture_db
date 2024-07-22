from app import create_app

if __name__ == '__main__':
   
    # Create the app with no prefix for local running
    app = create_app('/')
    
    # Run the app
    app.run_server(host="0.0.0.0", port=8050, debug=True)