from flask import Blueprint, render_template, current_app, request, redirect, url_for, session

student_routes = Blueprint('student_routes', __name__, template_folder='templates')

@student_routes.route('/student')
def student():
    mysql = current_app.config['mysql']  # MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    cur = mysql.connection.cursor()
    
    # Access session data
    if 'loggedin' in session and session['loggedin']:
        username = session['username']
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))
    
    # Execute a SELECT query to get the courses from the database
    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()

    return render_template('student.html', username=username, courses=courses)

@student_routes.route('/course-details/<int:course_id>')
def course_details(course_id):
    mysql = current_app.config['mysql']

    # Access session data
    if 'loggedin' not in session or not session['loggedin']:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

    course_info = get_course_details(mysql, course_id)
    return render_template('course_details.html', course_info=course_info)

# TODO: Adds course that you clicked to schedule
@student_routes.route('/add_course_to_schedule', methods=['POST'])
def add_course_to_schedule():
     mysql = current_app.config['mysql']
     if request.method == 'POST':
         name = request.form['name']
          

def get_student_schedule(mysql, student_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT c.course_id, c.name FROM Courses c JOIN Student_Courses sc ON c.course_id = sc.course_id WHERE sc.student_id = %s", (student_id,))
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    return schedule

def get_course_details(mysql, course_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT c.course_id, c.name, CONCAT(p.f_name, ' ', p.l_name) as professor, c.info, CONCAT(c.time, ' at Building ', c.building_id, ', Room ', c.room_id) as time_location FROM Courses c JOIN Professor p ON c.professor_id = p.professor_id WHERE c.course_id = %s", (course_id,))
    course_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return course_info
