from flask import Flask, jsonify, render_template, request, url_for, redirect, flash, abort
from werkzeug.exceptions import abort
import sqlite3
import logging

# Initialize connection count
connection_count = 0

# Configure logging
logging.basicConfig(
    filename='techtrends.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Function to get a database connection.
# This function connects to a database with the name `database.db`
def get_db_connection():
    global connection_count  # Use the global connection count variable
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1  # Increment connection count
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found, a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    try:
        post = get_post(post_id)
        if post is None:
            logging.warning(
                f"Article with ID {post_id} not found. Returning a 404 page."
            )
            return render_template('404.html'), 404
        else:
            logging.info(post["title"])
            return render_template('post.html', post=post)
    except Exception as e:
        abort(500)


# Define the About Us page
@app.route('/about')
def about():
    logging.info("About Us")
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    try:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            if not title:
                flash('Title is required!')
            else:
                logging.info(title)
                connection = get_db_connection()
                connection.execute(
                    'INSERT INTO posts (title, content) VALUES (?, ?)',
                    (title, content)
                )
                connection.commit()
                connection.close()

                return redirect(url_for('index'))

        return render_template('create.html')
    except Exception as e:
        abort(500)


# Define the health endpoint /healthz
@app.route('/healthz')
def health():
    try:
        get_db_connection()
        return jsonify({"result": "OK - healthy"})
    except Exception as e:
        abort(500)


# Define the metrics endpoint /metrics
@app.route('/metrics')
def metrics():
    try:
        connection = get_db_connection()
        posts = connection.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        connection.close()
        return jsonify({
            "status_code": 200,
            "db_connection_count": connection_count,
            "post_count": posts
        })
    except Exception as e:
        abort(500)


# Start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111)
