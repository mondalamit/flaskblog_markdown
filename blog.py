import os
from flask import Flask, render_template, g, abort
import sqlite3
import markdown

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'blog.db'),
    DEBUG=True,
    SECRET_KEY='this should probably be a secret',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('BLOG_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.template_filter('markdown') 
def markdown_filter(data):
    from flask import Markup
    from markdown import markdown
    return Markup(markdown(data))

@app.template_filter('snakeurl')
def snakeurl_filter(data):
    data = data.replace(' ', '-')
    data = data.lower()
    return data 

@app.route('/')
def index():
    entries = query_db('select * from entries')
    return render_template('blog.html', entries=entries)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/posts/<author>/<id>')
def view_single_post(author, id):
    author = author.replace('-', ' ')
    author = author.title()
    print(author)
    entry = query_db('select title, author, content from entries where author = ? and id = ?', [(author), (id)], one=True)
    if entry is None:
        abort(404)
    else:
        title = entry[0]
        author = entry[1]
        content = markdown.markdown(entry[2])
        return render_template('entry.html', title=title, author=author, content=content)