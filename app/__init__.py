#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================


from click import Group, password_option
from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import html
import secrets
import string
from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth    import login_required
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    if session.get("logged_in"):
        return redirect("/main")

    return render_template("pages/home.jinja")

#-----------------------------------------------------------
# Welcome page route
#-----------------------------------------------------------
@app.get("/main")
def main():
    with connect_db() as client:
        user_id = session.get("id")

        # Get all the things from the DB
        sql = """
            SELECT id, name, pass_key
            FROM `group`
            WHERE creator = ?
            ORDER BY name ASC
        """
        params=[user_id]
        result = client.execute(sql, params)
        owned_groups = result.rows


        # Get all the things from the DB
        sql = """
            SELECT id, name
            FROM `group`
            JOIN membership ON membership.group_id = `group`.id
            WHERE membership.user_id = ?
            ORDER BY name ASC
        """
        params=[user_id]
        result = client.execute(sql, params)
        member_groups = result.rows

        # And show them on the page
        return render_template("pages/main.jinja", owned_groups=owned_groups, member_groups=member_groups)



#-----------------------------------------------------------
# Join group page route
#-----------------------------------------------------------
@app.get("/join")
def join_group():
    return render_template("pages/join_group.jinja")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/creator")
def group_creator():
    return render_template("pages/group_creator.jinja")


# Function to generate a secure random password
def generate_password(length=7):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Create group rout
#-----------------------------------------------------------
@app.post("/create-group")
@login_required
def create_group(): 
    # Get the data from the form
    name = request.form.get("group_name")
   

    with connect_db() as client:

        # Attempt to find an existing record for that user
        sql = "SELECT * FROM `group` WHERE name = ?"
        params = [name]
        result = client.execute(sql, params)

        # No existing record found, so safe to add the user
        if not result.rows:

            # Generate a random password
            pass_key = generate_password()

            # Add the user to the users table
            sql = "INSERT INTO `group` (name,pass_key, creator) VALUES (?, ?, ?)"
            params = [name,pass_key, session["id"]]
            client.execute(sql, params)

            # And let them know it was successful and they can login
            flash("Group created", "success")
            return redirect("/main")

        # Found an existing record, so prompt to try again
        flash("Group already exist pls try again", "error")
        return redirect("/creator")


#-----------------------------------------------------------
# Join group page route
#-----------------------------------------------------------
@app.post("/join-group")
@login_required
def join():
     # Get the login form data
    submitted_pass_key = request.form.get("pass_key")

    with connect_db() as client:
        # Attempt to find a record for that group using the plaintext passkey
        sql = "SELECT * FROM `group` WHERE pass_key = ?"
        params = [submitted_pass_key]
        result = client.execute(sql, params)

        # Did we find a record?
        if result.rows:
            group = result.rows[0]
            
            # Since the database has a plaintext passkey, no hashing check is needed.
            # The database query already verified the passkey.
           
            # Save group info in the session
            group_id = group["id"]
            user_id = session["id"]

            # Add the user to the group
            sql = "INSERT INTO `membership` (group_id, user_id) VALUES (?, ?)"
            params = [group_id, user_id]
            client.execute(sql, params)            

            flash("Successfully joined the group!", "success")
            return redirect("/main")

        # No group found with that passkey
        flash("Group does not exist or incorrect passkey", "error")
        return redirect("/main")




#-----------------------------------------------------------
# Join group page route
#-----------------------------------------------------------
@app.get("/group/<int:id>/add-task")
def add_task(id):
    return render_template("pages/add_task.jinja", group_id=id)


 
#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
# - Restricted to logged in users
# #-----------------------------------------------------------
@app.post("/group/<int:id>/add-task")
@login_required
def add_a_task(id):

    # Get the data from the form
    task_name = request.form.get("task_name")
    descriptiom = request.form.get("description")
    time_stamp = request.form.get("time_stamp")
    maprunner_url = request.form.get("maprunner_url")

    # Sanitise the text inputst
    name = html.escape(task_name)
    name = html.escape(descriptiom)
    name = html.escape(time_stamp)
    name = html.escape(maprunner_url)

    # Get the user id from the session
    user_id = session["id"]
    group_id = id

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO tasks (task_name, description, time_stamp, maprunner_url, group_id ,user_id) VALUES (?, ?, ?, ?, ?, ?)"
        params = [task_name, descriptiom, time_stamp, maprunner_url, group_id, user_id]
        client.execute(sql, params)

        # Go back to the home page
        return redirect("/main")


# #-----------------------------------------------------------
# # Things page route - Show all the things, and new thing form
# #-----------------------------------------------------------
# @app.get("/things/")
# def show_all_things():
#     with connect_db() as client:
#         # Get all the things from the DB
#         sql = """
#             SELECT things.id,
#                    things.name,
#                    users.name AS owner

#             FROM things
#             JOIN users ON things.user_id = users.id

#             ORDER BY things.name ASC
#         """
#         params=[]
#         result = client.execute(sql, params)
#         things = result.rows

#         # And show them on the page
#         return render_template("pages/things.jinja", things=things)


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/group/<int:id>")
def show_group_info(id):
    with connect_db() as client:
        # Get the thing details from the DB, including the owner info
        sql = """
            SELECT 
               id, 
               name, 
               pass_key

            FROM `group`
            WHERE id = ?
        """
        params = [id,]
        result = client.execute(sql, params)
        my_group = result.rows[0]
    
        # Did we get a result?
        # yes, so show it on the page
            
        return render_template("pages/group.jinja", my_group=my_group)



#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
# - Restricted to logged in users
# #-----------------------------------------------------------
# @app.post("/add")
# @login_required
# def add_a_thing():
#     # Get the data from the form
#     name  = request.form.get("name")
#     price = request.form.get("price")

#     # Sanitise the text inputst
#     name = html.escape(name)

#     # Get the user id from the session
#     user_id = session["user_id"]

#     with connect_db() as client:
#         # Add the thing to the DB
#         sql = "INSERT INTO things (name, price, user_id) VALUES (?, ?, ?)"
#         params = [name, price, user_id]
#         client.execute(sql, params)

#         # Go back to the home page
#         flash(f"Thing '{name}' added", "success")
#         return redirect("/things")


# #-----------------------------------------------------------
# # Route for deleting a thing, Id given in the route
# # - Restricted to logged in users
# #-----------------------------------------------------------
# @app.get("/delete/<int:id>")
# @login_required
# def delete_a_thing(id):
#     # Get the user id from the session
#     user_id = session["user_id"]

#     with connect_db() as client:
#         # Delete the thing from the DB only if we own it
#         sql = "DELETE FROM things WHERE id=? AND user_id=?"
#         params = [id, user_id]
#         client.execute(sql, params)

#         # Go back to the home page
#         flash("Thing deleted", "success")
#         return redirect("/things")







#-----------------------------------------------------------
# User registration form route
#-----------------------------------------------------------
@app.get("/sign_up")
def register_form():
    return render_template("pages/sign_up.jinja")


#-----------------------------------------------------------
# User login form route
#-----------------------------------------------------------
@app.get("/sign_in")
def login_form():
    return render_template("pages/sign_in.jinja")


#-----------------------------------------------------------
# Route for adding a user when registration form submitted
#-----------------------------------------------------------
@app.post("/add-user")
def add_user():
    # Get the data from the form
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find an existing record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # No existing record found, so safe to add the user
        if not result.rows:
            # Sanitise the name
            name = html.escape(name)

            # Salt and hash the password
            hash = generate_password_hash(password)

            # Add the user to the users table
            sql = "INSERT INTO users (name, username, password_hash) VALUES (?, ?, ?)"
            params = [name, username, hash]
            client.execute(sql, params)

            # And let them know it was successful and they can login
            flash("Registration successful", "success")
            return redirect("/sign_in")

        # Found an existing record, so prompt to try again
        flash("Username already exists. Try again...", "error")
        return redirect("/sign_up")


#-----------------------------------------------------------
# Route for processing a user login
#-----------------------------------------------------------
@app.post("/login-user")
def login_user():
    # Get the login form data
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find a record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # Did we find a record?
        if result.rows:
            # Yes, so check password
            user = result.rows[0]
            hash = user["password_hash"]

            # Hash matches?
            if check_password_hash(hash, password):
                # Yes, so save info in the session

                print(user["id"])

                session["id"] = user["id"]
                session["user_name"] = user["name"]
                session["logged_in"] = True

                # And head back to the home page
                # flash("Login successful", "success")
                return redirect("/main")

        # Either username not found, or password was wrong
        flash("Invalid credentials", "error")
        return redirect("/sign_in")


#-----------------------------------------------------------
# Route for processing a user logout
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    # Clear the details from the session
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("logged_in", None)

    # And head back to the home page
    flash("Logged out successfully", "success")
    return redirect("/")
