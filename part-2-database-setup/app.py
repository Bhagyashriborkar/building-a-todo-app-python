# =============================================================================
# Part 2: Database Setup
# =============================================================================
# Now we add a database to store data permanently.
# We will learn:
#   1. What is SQLAlchemy (database toolkit)
#   2. How to create database models (tables)
#   3. How to query the database
# =============================================================================



from flask import Flask, render_template
import os
from models import db, User, Todo, init_db

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# =============================================================================
# DATABASE SETUP
# =============================================================================
def setup_database():
    """Setup database with fresh tables"""
    print("Setting up database...")
    
    # Create instance folder if it doesn't exist
    instance_path = 'instance'
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"Created {instance_path} folder")
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Create test data if no users exist
        if User.query.count() == 0:
            create_test_data()
    
    return True

def create_test_data():
    """Create sample data for testing"""
    print("Creating test data...")
    
    try:
        # Create users with phone numbers
        user1 = User(
            username='alice', 
            email='alice@example.com', 
            password_hash='temp123', 
            phone_no='1111111111'
        )
        user2 = User(
            username='bob', 
            email='bob@example.com', 
            password_hash='temp456', 
            phone_no='2222222222'
        )
        user3 = User(
            username='charlie', 
            email='charlie@example.com', 
            password_hash='temp789', 
            phone_no='3333333333'
        )
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print(" 3 users created")

        # Create todos
        todo1 = Todo(task_content='Learn Flask', user_id=user1.id)
        todo2 = Todo(task_content='Learn SQLAlchemy', user_id=user1.id)
        todo3 = Todo(task_content='Build Todo App', user_id=user2.id)
        todo4 = Todo(task_content='Test Database', user_id=user3.id)
        todo5 = Todo(task_content='Deploy Application', user_id=user3.id, is_completed=True)

        db.session.add_all([todo1, todo2, todo3, todo4, todo5])
        db.session.commit()
        print(" 5 todos created")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.session.rollback()

# =============================================================================
# ROUTES
# =============================================================================
@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    """Test database page"""
    try:
        with app.app_context():
            all_users = User.query.all()
            all_todos = Todo.query.all()
            user_count = User.query.count()
            
            print(f"Found {user_count} users and {len(all_todos)} todos")
            
            return render_template(
                'test_db.html',
                users=all_users,
                todos=all_todos,
                user_count=user_count
            )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/reset-db')
def reset_db():
    """Reset database (for testing)"""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("All tables dropped")
        
        # Recreate tables
        db.create_all()
        print("All tables recreated")
        
        # Create test data
        create_test_data()
        
    return "Database reset successfully! <a href='/test-db'>View Database</a>"

# =============================================================================
# RUN THE SERVER
# =============================================================================
if __name__ == '__main__':
    # Setup database before running
    setup_database()
    
    print("\n" + "="*60)
    print("   TODO APP - PART 2: DATABASE SETUP")
    print("="*60)
    print("  Database: SQLite with phone_no column")
    print("   Models: Users, Todos with relationships")
    print("  Test Data: 3 users, 5 todos created")
    print("="*60)
    print("  Home Page:    http://127.0.0.1:5000")
    print("   Test DB:      http://127.0.0.1:5000/test-db")
    print("  Reset DB:     http://127.0.0.1:5000/reset-db")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)

# ============================================
# SELF-STUDY QUESTIONS
# ============================================
# 1. What is SQLAlchemy and why do we use it?
# 2. What does db.Column(db.String(80)) mean?
# 3. What is the difference between db.session.add() and db.session.commit()?
# 4. What does filter_by() do? How is it different from get()?
# 5. What happens if you delete todo.db file and restart the app?
#
# ============================================
# ACTIVITIES - Try These!
# ============================================
# Activity 1: Add a new field
#   - In models.py, add 'phone' field to User model
#   - Delete todo.db file (so tables are recreated)
#   - Restart the app and check if it works
#
# Activity 2: Query practice
#   - In test_db route, try: User.query.all() (gets all users)
#   - Try: User.query.first() (gets first user)
#   - Try: User.query.count() (counts users)
#
# Activity 3: View database file
#   - Install "DB Browser for SQLite" software
#   - Open instance/todo.db file
#   - See the tables and data inside
#
# Activity 4: Add more test data
#   - Modify test_db() to create 3 users instead of 1
#   - Create different todos for each user
# ============================================
