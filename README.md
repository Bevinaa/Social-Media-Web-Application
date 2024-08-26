# Social Media Application Using Python Flask

This is a social media web application built using Flask. It allows users to sign up, log in, create posts, upload images, and follow other users. The app also implements various data structures for user interaction and maintains a user's social connections.

## Features

- **User Authentication:** Users can sign up, log in, and manage their accounts.
- **Post Creation:** Users can create posts with captions and upload images.
- **Social Features:** Users can follow and be followed by others. Notifications are sent when someone gains a follower.
- **Profile Management:** Users can view their profiles, see their followers, following counts, and upload profile pictures.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bevinaa/Social-Media-Web-Application.git
   ```
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the app:**
   Visit `http://localhost:5000` in your web browser.

## File Structure

- **app.py:** The main application file containing all the routes and logic.
- **templates/:** Directory containing HTML files for rendering different pages.
- **uploads/:** Directory for storing uploaded images.

## Key Routes

- `/`: Home page
- `/login`: User login
- `/signup`: User registration
- `/create_account`: Final step for account creation
- `/my_feed/<user_id>`: User feed page
- `/my_profile/<user_id>`: User profile page
- `/add_post`: Create a new post
- `/follow/<followed_user_id>`: Follow another user
- `/upload_profile_pic`: Upload profile picture

## Data Persistence

User data, posts, usernames, and emails are stored using pickle files:

- **user_data.pkl:** Stores user information such as ID, name, email, etc.
- **usernames.pkl:** Stores registered usernames.
- **emails.pkl:** Stores registered email addresses.
- **user_posts.pkl:** Stores user posts.

## Image Uploads

Images uploaded by users are stored in the `uploads/` directory, and secure filenames are generated using `werkzeug.utils.secure_filename`.

## Notifications

The application uses session-based notifications to alert users of new followers.

## Contributions

Feel free to fork this repository and submit pull requests to contribute to the project.
