"""
==========================================================
AI & DS Department Website - Flask Backend
==========================================================
This is the main Flask application file that provides:
1. API endpoint to receive and store contact form data
2. API endpoint to fetch faculty details
3. SQLite database for data storage
==========================================================
"""

# ========================================
# Import Required Libraries
# ========================================
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # For handling Cross-Origin requests
import sqlite3
import os
from datetime import datetime

# ========================================
# Initialize Flask Application
# ========================================
app = Flask(__name__, static_folder='.')  # Serve static files from current directory
CORS(app)  # Enable CORS for all routes (allows frontend to connect)

# Database file path
DATABASE = 'department.db'

# ========================================
# Database Helper Functions
# ========================================

def get_db_connection():
    """
    Create and return a database connection.
    Uses Row factory to return rows as dictionaries.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This makes rows accessible by column name
    return conn


def init_db():
    """
    Initialize the database with required tables.
    Creates tables if they don't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ----------------------------------------
    # Create Contact Messages Table
    # Stores all contact form submissions
    # ----------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            newsletter INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ----------------------------------------
    # Create Faculty Table
    # Stores faculty member information
    # ----------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            designation TEXT NOT NULL,
            subject TEXT NOT NULL,
            bio TEXT,
            email TEXT,
            is_hod INTEGER DEFAULT 0
        )
    ''')
    
    # ----------------------------------------
    # Create Achievements Table
    # Stores achievements shown in ticker
    # ----------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icon TEXT DEFAULT '🏆',
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ----------------------------------------
    # Create Gallery Table
    # Stores event images with captions
    # ----------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT NOT NULL,
            caption TEXT NOT NULL,
            event_date TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if gallery table is empty, if so, add sample data
    cursor.execute('SELECT COUNT(*) FROM gallery')
    gallery_count = cursor.fetchone()[0]
    
    if gallery_count == 0:
        sample_gallery = [
            ('https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600', 'Annual Tech Fest 2024 - Students showcasing AI projects', '2024-03-15'),
            ('https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=600', 'Industry Expert Guest Lecture on Machine Learning', '2024-02-20'),
            ('https://images.unsplash.com/photo-1559223607-a43c990c692c?w=600', 'Hackathon Winners - Smart India Hackathon 2024', '2024-01-10'),
            ('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600', 'Workshop on Deep Learning and Neural Networks', '2024-02-05'),
            ('https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600', 'Placement Drive - Campus Recruitment 2024', '2024-01-25'),
            ('https://images.unsplash.com/photo-1552664730-d307ca884978?w=600', 'Faculty Development Program on AI Ethics', '2024-02-28'),
        ]
        cursor.executemany('''
            INSERT INTO gallery (image_url, caption, event_date)
            VALUES (?, ?, ?)
        ''', sample_gallery)
        print("✅ Sample gallery data inserted!")
    
    # Check if achievements table is empty, if so, add sample data
    cursor.execute('SELECT COUNT(*) FROM achievements')
    ach_count = cursor.fetchone()[0]
    
    if ach_count == 0:
        sample_achievements = [
            ('🎯', '100% Placement', 'All eligible students placed in top MNCs for 2024 batch', 'placement', 1),
            ('💼', 'Top Recruiters', 'Google, Microsoft, Amazon, TCS, Infosys & more visiting campus', 'placement', 1),
            ('🏆', 'Hackathon Champions', 'Students won Smart India Hackathon 2024', 'competition', 1),
            ('📚', 'Research Excellence', '50+ papers published in international journals', 'research', 1),
            ('🌟', 'Industry Projects', 'Live projects with IBM, Intel & Nvidia partnerships', 'project', 1),
            ('🎓', 'Highest Package', '45 LPA offered by leading tech company', 'placement', 1),
        ]
        cursor.executemany('''
            INSERT INTO achievements (icon, title, description, category, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_achievements)
        print("✅ Sample achievements data inserted!")
    
    # Check if faculty table is empty, if so, add sample data
    cursor.execute('SELECT COUNT(*) FROM faculty')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert sample faculty data
        sample_faculty = [
            ('Dr. Rajesh Kumar', 'Head of Department & Professor', 
             'Deep Learning & Neural Networks',
             'Dr. Rajesh Kumar has over 20 years of experience in AI research and education.',
             'rajesh.kumar@college.edu', 1),
            ('Dr. Priya Sharma', 'Associate Professor',
             'Machine Learning & Pattern Recognition',
             'Ph.D. from IISc Bangalore with expertise in ML algorithms.',
             'priya.sharma@college.edu', 0),
            ('Dr. Amit Patel', 'Associate Professor',
             'Natural Language Processing',
             'Expert in NLP with focus on sentiment analysis and language models.',
             'amit.patel@college.edu', 0),
            ('Dr. Sneha Reddy', 'Assistant Professor',
             'Computer Vision & Image Processing',
             'Specializes in image recognition and object detection algorithms.',
             'sneha.reddy@college.edu', 0),
            ('Dr. Vikram Singh', 'Assistant Professor',
             'Big Data Analytics',
             'Expert in distributed computing and large-scale data processing.',
             'vikram.singh@college.edu', 0),
            ('Dr. Anita Verma', 'Assistant Professor',
             'Data Mining & Warehousing',
             'Focuses on knowledge discovery from large datasets.',
             'anita.verma@college.edu', 0),
            ('Prof. Dhanapathy', 'Professor',
             'Artificial Neural Networks',
             '30+ years of teaching experience with expertise in neural networks.',
             'dhanapathy@college.edu', 0),
            ('Dr. Kavita Nair', 'Associate Professor',
             'Reinforcement Learning',
             'Research focuses on RL applications in robotics.',
             'kavita.nair@college.edu', 0),
            ('Dr. Rahul Joshi', 'Assistant Professor',
             'Statistical Learning & Probability',
             'Expert in probabilistic models and statistical inference.',
             'rahul.joshi@college.edu', 0),
        ]
        
        cursor.executemany('''
            INSERT INTO faculty (name, designation, subject, bio, email, is_hod)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_faculty)
        print("✅ Sample faculty data inserted!")
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


# ========================================
# API Routes
# ========================================

# ----------------------------------------
# Route: Serve Static Files (Frontend)
# ----------------------------------------
@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve any static file (HTML, CSS, JS)"""
    return send_from_directory('.', filename)


# ----------------------------------------
# Route: Admin Login
# POST /api/login
# ----------------------------------------
# Admin credentials (In production, use environment variables and hashed passwords)
ADMIN_CREDENTIALS = {
    'admin': 'smvec2024',
    'staff': 'aidsstaff123'
}

@app.route('/api/login', methods=['POST'])
def admin_login():
    """
    Authenticate admin/staff login.
    
    Expected JSON body:
    {
        "username": "admin",
        "password": "smvec2024"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip().lower()
        password = data.get('password', '')
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': username
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Submit Contact Form
# POST /api/contact
# ----------------------------------------
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """
    Receive contact form data and store in database.
    
    Expected JSON body:
    {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "subject": "admission",
        "message": "I want to know about...",
        "newsletter": true
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert contact message
        cursor.execute('''
            INSERT INTO contact_messages 
            (first_name, last_name, email, phone, subject, message, newsletter)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['firstName'],
            data['lastName'],
            data['email'],
            data.get('phone', ''),
            data['subject'],
            data['message'],
            1 if data.get('newsletter') else 0
        ))
        
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Your message has been received! We will get back to you soon.',
            'id': message_id
        }), 201
        
    except Exception as e:
        # Return error response
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Get All Contact Messages
# GET /api/contact
# ----------------------------------------
@app.route('/api/contact', methods=['GET'])
def get_contacts():
    """
    Fetch all contact messages from database.
    Returns list of all submitted contact forms.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
        messages = cursor.fetchall()
        conn.close()
        
        # Convert rows to list of dictionaries
        result = []
        for msg in messages:
            result.append({
                'id': msg['id'],
                'firstName': msg['first_name'],
                'lastName': msg['last_name'],
                'email': msg['email'],
                'phone': msg['phone'],
                'subject': msg['subject'],
                'message': msg['message'],
                'newsletter': bool(msg['newsletter']),
                'createdAt': msg['created_at']
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Get All Faculty Members
# GET /api/faculty
# ----------------------------------------
@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """
    Fetch all faculty members from database.
    Returns list of faculty with their details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all faculty, HOD first
        cursor.execute('SELECT * FROM faculty ORDER BY is_hod DESC, name ASC')
        faculty = cursor.fetchall()
        conn.close()
        
        # Convert rows to list of dictionaries
        result = []
        for member in faculty:
            result.append({
                'id': member['id'],
                'name': member['name'],
                'designation': member['designation'],
                'subject': member['subject'],
                'bio': member['bio'],
                'email': member['email'],
                'isHod': bool(member['is_hod'])
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Get Single Faculty Member
# GET /api/faculty/<id>
# ----------------------------------------
@app.route('/api/faculty/<int:faculty_id>', methods=['GET'])
def get_faculty_by_id(faculty_id):
    """
    Fetch a single faculty member by ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM faculty WHERE id = ?', (faculty_id,))
        member = cursor.fetchone()
        conn.close()
        
        if member is None:
            return jsonify({
                'success': False,
                'error': 'Faculty member not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': member['id'],
                'name': member['name'],
                'designation': member['designation'],
                'subject': member['subject'],
                'bio': member['bio'],
                'email': member['email'],
                'isHod': bool(member['is_hod'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Add New Faculty Member
# POST /api/faculty
# ----------------------------------------
@app.route('/api/faculty', methods=['POST'])
def add_faculty():
    """
    Add a new faculty member to database.
    
    Expected JSON body:
    {
        "name": "Dr. New Faculty",
        "designation": "Assistant Professor",
        "subject": "Machine Learning",
        "bio": "Expert in ML...",
        "email": "faculty@college.edu",
        "isHod": false
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'designation', 'subject']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO faculty (name, designation, subject, bio, email, is_hod)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['designation'],
            data['subject'],
            data.get('bio', ''),
            data.get('email', ''),
            1 if data.get('isHod') else 0
        ))
        
        conn.commit()
        faculty_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Faculty member added successfully!',
            'id': faculty_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Update Faculty Member
# PUT /api/faculty/<id>
# ----------------------------------------
@app.route('/api/faculty/<int:faculty_id>', methods=['PUT'])
def update_faculty(faculty_id):
    """Update an existing faculty member."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE faculty SET 
                name = ?, designation = ?, subject = ?, bio = ?, email = ?, is_hod = ?
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('designation'),
            data.get('subject'),
            data.get('bio', ''),
            data.get('email', ''),
            1 if data.get('isHod') else 0,
            faculty_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Faculty member updated successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Delete Faculty Member
# DELETE /api/faculty/<id>
# ----------------------------------------
@app.route('/api/faculty/<int:faculty_id>', methods=['DELETE'])
def delete_faculty(faculty_id):
    """Delete a faculty member."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM faculty WHERE id = ?', (faculty_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Faculty member deleted successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Get All Achievements
# GET /api/achievements
# ----------------------------------------
@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Fetch all achievements for the ticker."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get active achievements by default, or all if ?all=true
        show_all = request.args.get('all', 'false').lower() == 'true'
        
        if show_all:
            cursor.execute('SELECT * FROM achievements ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM achievements WHERE is_active = 1 ORDER BY created_at DESC')
        
        achievements = cursor.fetchall()
        conn.close()
        
        result = []
        for ach in achievements:
            result.append({
                'id': ach['id'],
                'icon': ach['icon'],
                'title': ach['title'],
                'description': ach['description'],
                'category': ach['category'],
                'isActive': bool(ach['is_active']),
                'createdAt': ach['created_at']
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Add New Achievement
# POST /api/achievements
# ----------------------------------------
@app.route('/api/achievements', methods=['POST'])
def add_achievement():
    """Add a new achievement to the ticker."""
    try:
        data = request.get_json()
        
        if not data.get('title') or not data.get('description'):
            return jsonify({
                'success': False,
                'error': 'Title and description are required'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO achievements (icon, title, description, category, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('icon', '🏆'),
            data['title'],
            data['description'],
            data.get('category', 'general'),
            1 if data.get('isActive', True) else 0
        ))
        
        conn.commit()
        ach_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Achievement added successfully!',
            'id': ach_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Update Achievement
# PUT /api/achievements/<id>
# ----------------------------------------
@app.route('/api/achievements/<int:ach_id>', methods=['PUT'])
def update_achievement(ach_id):
    """Update an existing achievement."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE achievements SET 
                icon = ?, title = ?, description = ?, category = ?, is_active = ?
            WHERE id = ?
        ''', (
            data.get('icon', '🏆'),
            data.get('title'),
            data.get('description'),
            data.get('category', 'general'),
            1 if data.get('isActive', True) else 0,
            ach_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Achievement updated successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Delete Achievement
# DELETE /api/achievements/<id>
# ----------------------------------------
@app.route('/api/achievements/<int:ach_id>', methods=['DELETE'])
def delete_achievement(ach_id):
    """Delete an achievement."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM achievements WHERE id = ?', (ach_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Achievement deleted successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Get All Gallery Images
# GET /api/gallery
# ----------------------------------------
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Fetch all gallery images."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        show_all = request.args.get('all', 'false').lower() == 'true'
        
        if show_all:
            cursor.execute('SELECT * FROM gallery ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM gallery WHERE is_active = 1 ORDER BY created_at DESC')
        
        images = cursor.fetchall()
        conn.close()
        
        result = []
        for img in images:
            result.append({
                'id': img['id'],
                'imageUrl': img['image_url'],
                'caption': img['caption'],
                'eventDate': img['event_date'],
                'isActive': bool(img['is_active']),
                'createdAt': img['created_at']
            })
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Add New Gallery Image
# POST /api/gallery
# ----------------------------------------
@app.route('/api/gallery', methods=['POST'])
def add_gallery():
    """Add a new gallery image."""
    try:
        data = request.get_json()
        
        if not data.get('imageUrl') or not data.get('caption'):
            return jsonify({
                'success': False,
                'error': 'Image URL and caption are required'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO gallery (image_url, caption, event_date, is_active)
            VALUES (?, ?, ?, ?)
        ''', (
            data['imageUrl'],
            data['caption'],
            data.get('eventDate', ''),
            1 if data.get('isActive', True) else 0
        ))
        
        conn.commit()
        img_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Gallery image added successfully!',
            'id': img_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Update Gallery Image
# PUT /api/gallery/<id>
# ----------------------------------------
@app.route('/api/gallery/<int:img_id>', methods=['PUT'])
def update_gallery(img_id):
    """Update an existing gallery image."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE gallery SET 
                image_url = ?, caption = ?, event_date = ?, is_active = ?
            WHERE id = ?
        ''', (
            data.get('imageUrl'),
            data.get('caption'),
            data.get('eventDate', ''),
            1 if data.get('isActive', True) else 0,
            img_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Gallery image updated successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ----------------------------------------
# Route: Delete Gallery Image
# DELETE /api/gallery/<id>
# ----------------------------------------
@app.route('/api/gallery/<int:img_id>', methods=['DELETE'])
def delete_gallery(img_id):
    """Delete a gallery image."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM gallery WHERE id = ?', (img_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Gallery image deleted successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========================================
# Run the Application
# ========================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting AI & DS Department Backend Server")
    print("="*50)
    
    init_db()
    
    print("\n📡 API Endpoints Available:")
    print("-" * 40)
    print("GET  /                     → Home page")
    print("GET  /api/faculty          → Get all faculty")
    print("POST /api/faculty          → Add faculty")
    print("PUT  /api/faculty/<id>     → Update faculty")
    print("DELETE /api/faculty/<id>   → Delete faculty")
    print("GET  /api/achievements     → Get achievements")
    print("POST /api/achievements     → Add achievement")
    print("PUT  /api/achievements/<id>→ Update achievement")
    print("DELETE /api/achievements   → Delete achievement")
    print("GET  /api/gallery          → Get gallery images")
    print("POST /api/gallery          → Add gallery image")
    print("PUT  /api/gallery/<id>     → Update gallery image")
    print("DELETE /api/gallery/<id>   → Delete gallery image")
    print("GET  /api/contact          → Get messages")
    print("POST /api/contact          → Submit contact")
    print("-" * 40)
    print("\n🌐 Server running at: http://localhost:5000")
    print("📁 Serving static files from current directory")
    print("\nPress Ctrl+C to stop the server\n")
    
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
