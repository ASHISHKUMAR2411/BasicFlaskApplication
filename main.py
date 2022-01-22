# jinja allow writing templates for the apps



from website import create_app
# import create_app will make it like an object as website is now an package
# Now after we build an instance of the create_app function, and run it main to work as the server

app = create_app()
if __name__ == '__main__':
    app.run(debug=False)
    # here debug=True means whenever we change the app files or any changes in the project it will re-render or re-run the whole file checking for error and if everything is good it will execute it

