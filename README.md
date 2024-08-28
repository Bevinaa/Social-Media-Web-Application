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

## Contact

For questions or further information, please contact:

- **Name:** Bevina R
- **Email:** bevina2110@gmail.com
- **GitHub:** [yourusername](https://github.com/Bevinaa)

## Output of the Project 

![Screenshot 2024-06-09 221535](https://github.com/user-attachments/assets/90a2b03c-8b19-417e-9077-7d4c775a39bd)

![Screenshot 2024-06-09 221707](https://github.com/user-attachments/assets/386741ce-a3d7-4a6a-b53b-8cd894105c51)

![Screenshot 2024-06-09 221849](https://github.com/user-attachments/assets/6ed29b87-6c03-43ff-a25f-1dae53276db5)

![Screenshot 2024-06-09 221949](https://github.com/user-attachments/assets/ee546bc1-b09f-4dab-97c2-19ed43651213)

![Screenshot 2024-06-09 222044](https://github.com/user-attachments/assets/c9b47816-f64f-4367-9812-60ec30ef3ed6)

![Screenshot 2024-06-09 222142](https://github.com/user-attachments/assets/3021b49e-ef57-44ee-ab99-40308207a5ef)

![Screenshot 2024-06-09 222219](https://github.com/user-attachments/assets/dd1691b9-ad54-4a17-815d-36e5e6cf846d)

![Screenshot 2024-06-09 222354](https://github.com/user-attachments/assets/69996e90-25b4-4906-8d87-33679bb7fb7d)

![Screenshot 2024-06-09 222549](https://github.com/user-attachments/assets/c283b759-8aef-44d1-ab15-63bdfdb16317)





