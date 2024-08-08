from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import pickle, os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from adsa import UserGraph,  TrieNode, SplayTree, LinkedList, Stack, Queue

app = Flask(__name__)
app.secret_key = '1234'

# User data file
USER_DATA_FILE = 'user_data.pkl'

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'rb') as file:
            return pickle.load(file)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump(user_data, file)

# Usernames file 
USERNAME_FILE = 'usernames.pkl'

if not os.path.exists(USERNAME_FILE):
    with open(USERNAME_FILE, 'wb') as file:
        pickle.dump([], file)

def load_username_file():
    try:
        with open(USERNAME_FILE, 'rb') as file:
            return pickle.load(file)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_username_file(user_data):
    with open(USERNAME_FILE, 'wb') as file:
        pickle.dump(user_data, file)

# Emails file
EMAIL_FILE = 'emails.pkl'

if not os.path.exists(EMAIL_FILE):
    with open(EMAIL_FILE, 'wb') as file:
        pickle.dump([], file)

def load_email_file():
    try:
        with open(EMAIL_FILE, 'rb') as file:
            return pickle.load(file)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_email_file(email_data):
    with open(EMAIL_FILE, 'wb') as file:
        pickle.dump(email_data, file)

#Save posted images
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
# Global dictionary for maintaining posts
user_posts = {}

# Iniatilizing Data Structures

splay = SplayTree() #max attempts
graph = UserGraph() #social connections
linkedlist = LinkedList() #my_profile posts
tree = TrieNode() #username, mail availability
stack = Stack()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
queue = Queue() 

#Routes  
@app.route("/")
def index():
    return render_template('first.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_data = load_user_data()
        
        print(f"User email: {user_email}")
        print(f"User password: {user_password}")
        print(f"User data: {user_data}")

        global splay
        max_attempts = 5
        flash("Cannot login now. Try after some time")

        for data in user_data:
            print(f"Checking data: {data}")
            if isinstance(data, dict) and data.get('email') == user_email and data.get('password') == user_password:
                user_id = data.get('id')
                if user_id:
                    print(f"User ID found: {user_id}")
                    session['user_id'] = user_id
                    session['username'] = data.get('username')  # Store username in session
                    return redirect(url_for('my_feed', user_id=user_id))
                else:
                    flash('User data is missing. Please contact support.', 'error')
                    return redirect(url_for('login'))

        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']

        existing_users = load_user_data()
        if any(user['email'] == user_email for user in existing_users):
            flash('Email already registered. Please use another email.', 'error')
            return redirect(url_for('signup'))

        session['temp_user'] = {
            'name': user_name,
            'email': user_email,
            'password': user_password
        }

        return redirect(url_for('create_account'))

    return render_template('signup.html')

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        id_name = request.form['name']
        id_uname = request.form['uname']
        id_phone = request.form['phnno']
        id_email = request.form['email']
        id_age = request.form['age']
        id_gender = request.form['gender']

        if not all([id_name, id_uname, id_phone, id_email, id_age, id_gender]):
            flash('Please fill in all the required fields.', 'error')
            return render_template('create_account.html')

        data = load_username_file()
        if any(username_data['username'] == id_uname for username_data in data):
            flash('Username already taken. Try another username.', 'error')
            return render_template('create_account.html')

        emails = load_email_file()
        if any(user_email['user_email'] == id_email for user_email in emails):
            flash('Email already registered. Please use another email.', 'error')
            return render_template('create_account.html')

        temp_user = session.pop('temp_user', None)
        if not temp_user:
            flash('Session expired. Please sign up again.', 'error')
            return redirect(url_for('signup'))

        user_data = load_user_data()
        new_user_id = len(user_data) + 1

        user_details = {
            'id': new_user_id,
            'name': id_name,
            'username': id_uname,
            'phone': id_phone,
            'email': id_email,
            'age': id_age,
            'gender': id_gender,
            'password': temp_user['password'],
        }
        user_data.append(user_details)
        save_user_data(user_data)

        id_uname_data = {'username': id_uname}
        data.append(id_uname_data)
        save_username_file(data)

        id_email_data = {'user_email': id_email}
        emails.append(id_email_data)
        save_email_file(emails)

        session['name'] = id_name
        session['username'] = id_uname
        session['user_details'] = user_details
        session['user_email'] = id_email
        session['user_id'] = new_user_id
        
        return redirect(url_for('my_feed', user_id=new_user_id, user=user_details))

    temp_user = session.get('temp_user', {})
    return render_template('create_account.html', temp_user=temp_user)

@app.route('/check_email_availability/<email>')
def check_email_availability(email):
    global TrieNode
    email_data = load_email_file()
    if any(email_data['user_email'] == email for email_data in email_data):
        return jsonify({'available': False})
    else:
        return jsonify({'available': True})

@app.route('/check_username_availability/<username>')
def check_username_availability(username):
    global TrieNode
    data = load_username_file()
    if any(username_data['username'] == username for username_data in data):
        return jsonify({'available': False})
    else:
        return jsonify({'available': True})

@app.route('/my_feed/<int:user_id>', methods=['GET', 'POST'])
def my_feed(user_id):
    user_id = session.get('user_id')
    if user_id:
        posts = user_posts.get(user_id, [])
        user_data = load_user_data()  
        notifications = session.get('notifications', [])
        user_details = next((user for user in user_data if 'id' in user and user['id'] == user_id), None)
        if user_details:
            return render_template('my_feed.html', posts=posts, user=user_details, user_id=user_id, notifications=notifications)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('create_account'))
    else:
        flash('User not logged in.', 'error')
        return redirect(url_for('login'))


@app.route("/save_post", methods=['POST'])
def save_post():
    user_id = request.form.get('user_id')
    username = request.form['username']
    caption = request.form['caption']
    image = request.files['image']
    
    post_data = {'username': username, 'caption': caption, 'image_filename': image.filename}
    
    global user_posts
    if user_id in user_posts:
        user_posts[user_id].append(post_data)
    else:
        user_posts[user_id] = [post_data]
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Save the user_posts globally
    with open('user_posts.pkl', 'wb') as file:
        pickle.dump(user_posts, file)

    print(user_posts) #test

    return jsonify({'message': 'Post saved successfully'})

@app.route("/my_profile/<int:user_id>", methods=['GET', 'POST'])
def my_profile(user_id):
    global linkedlist
    user_data = load_user_data()
    user_details = next((user for user in user_data if 'id' in user and user['id'] == user_id), None)
    if user_details:
        following_count = len(user_details.get('following', []))
        followers_count = len(user_details.get('followers', []))
        user_posts_data = user_posts.get(str(user_id), [])
        post_count = len(user_posts_data)
        return render_template('my_profile.html', user=user_details, user_id=user_id, following_count=following_count, followers_count=followers_count ,post_count=post_count, user_posts=user_posts_data)
    else:
        flash('User not found.', 'error')
        return redirect(url_for('create_account'))

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_posts/<int:user_id>', methods=['GET'])
def get_posts(user_id):
    if user_id in user_posts:
        return jsonify(user_posts[user_id])
    else:
        return jsonify([])
    
@app.route("/social/<int:user_id>", methods=['GET', 'POST'])
def social(user_id):
    global UserGraph
    user_data = load_user_data()
    return render_template('social.html', user_data=user_data, user_id=user_id)

# Function to send notification
def send_notification(user_id, message):
    if 'notifications' not in session:
        session['notifications'] = []
    session['notifications'].append(message)

@app.route("/follow/<int:followed_user_id>", methods=['POST'])
def follow(followed_user_id):
    logged_in_user_id = session.get('user_id')

    if logged_in_user_id is None:
        flash('You need to be logged in to follow users.', 'error')
        return redirect(url_for('login'))

    user_data = load_user_data()

    logged_in_user = next((user for user in user_data if user['id'] == logged_in_user_id), None)
    followed_user = next((user for user in user_data if user['id'] == followed_user_id), None)

    if followed_user:
        message = f"You have a new follower: {logged_in_user['username']}"
        send_notification(followed_user_id, message)

    if logged_in_user and followed_user:
        if 'following' not in logged_in_user:
            logged_in_user['following'] = []
        if 'followers' not in followed_user:
            followed_user['followers'] = []

        if followed_user_id not in logged_in_user['following']:
            logged_in_user['following'].append(followed_user_id)
            followed_user['followers'].append(logged_in_user_id)
            save_user_data(user_data)
    else:
        flash('User not found.', 'error')

    return redirect(url_for('my_feed', user_id=logged_in_user_id))

@app.route("/add_post", methods=['GET', 'POST'])
def add_post():
    return render_template('add_post.html')

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'user_id' not in session:
        flash('User not logged in.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    if 'profile_pic' not in request.files:
        flash('No file part.', 'error')
        return redirect(url_for('my_profile', user_id=user_id))
    
    file = request.files['profile_pic']
    if file.filename == '':
        flash('No selected file.', 'error')
        return redirect(url_for('my_profile', user_id=user_id))
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user_data = load_user_data()
        for user in user_data:
            if user['id'] == user_id:
                user['profile_pic'] = filename
                break
        save_user_data(user_data)
        
        flash('Profile picture updated successfully.', 'success')
        return redirect(url_for('my_profile', user_id=user_id))
    
if __name__ == '__main__':
    app.run(debug=True)