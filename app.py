import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import AddPatientForm, DeletePatientForm, LoginForm, RegistrationForm, EditPatientForm
from config import Config

# setting flask
app = Flask(__name__)
app.config.from_object(Config)

# Db setup
db = SQLAlchemy(app)
Migrate(app, db)

# Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class Doctor(UserMixin, db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(user_id)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(50), nullable=False)  
    blood_type = db.Column(db.String(50), nullable=False)  
    birth_date = db.Column(db.Date, nullable=False, default='2000-01-01')
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)

    def __init__(self, name, gender,blood_type, birth_date ,doctor_id=None):
        self.name = name
        self.doctor_id = doctor_id
        self.gender = gender
        self.birth_date = birth_date
        self.blood_type = blood_type

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medications = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    vital_signs = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    treatment_plan = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, patient_id, medications=None, allergies=None, vital_signs=None, diagnosis=None, treatment_plan=None, description=None):
        self.patient_id = patient_id
        self.medications = medications
        self.allergies = allergies
        self.vital_signs = vital_signs
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan
        self.description = description


# Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        doctor = Doctor(username=form.username.data, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))
    elif form.errors:  # Check if there are validation errors
        for field, error_list in form.errors.items():
            for error in error_list:
                flash(f"{field.capitalize()}: {error}", "danger")  # Display errors with flash messages
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(username=form.username.data).first()
        if doctor and check_password_hash(doctor.password, form.password.data):
            login_user(doctor)
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password. Try again.", "danger")
    elif form.errors:  # Check if there are validation errors
        for field, error_list in form.errors.items():
            for error in error_list:
                flash(f"{field.capitalize()}: {error}", "danger")  # Display errors with flash messages
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        name = form.name.data
        gender = form.gender.data  # Get gender from the form
        birth_date = form.birth_date.data  # New field
        blood_type = form.blood_type.data  # Get blood type from the form
        doctor_id = current_user.id

        # Create a new patient object with all required fields
        new_patient = Patient(name=name, gender=gender, birth_date=birth_date, blood_type=blood_type, doctor_id=doctor_id)
        db.session.add(new_patient)
        db.session.commit()
        
        flash("Patient added successfully!", "success")
        return redirect(url_for('list_patients'))
    return render_template('add.html', form=form)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):

    patient = Patient.query.filter_by(id=patient_id, doctor_id=current_user.id).first()
    

    if not patient:
        flash("Unauthorized access or patient not found.", "danger")
        return redirect(url_for('list_patients'))
    
    form = EditPatientForm(obj=patient)  
    
    if form.validate_on_submit():

        patient.name = form.name.data
        patient.gender = form.gender.data
        patient.birth_date = form.birth_date.data
        patient.blood_type = form.blood_type.data
        

        db.session.commit()
        
        flash("Patient details updated successfully!", "success")
        return redirect(url_for('list_patients'))
    
    return render_template('edit_patient.html', form=form, patient=patient)


# you list the patients
@app.route('/list')
@login_required
def list_patients():
    patients = Patient.query.filter_by(doctor_id=current_user.id).all()
    return render_template('list.html', patients=patients)

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_patient():
    form = DeletePatientForm()
    if form.validate_on_submit():
        patient_id = form.id.data
        patient = Patient.query.filter_by(id=patient_id, doctor_id=current_user.id).first()
        if patient:
            db.session.delete(patient)
            db.session.commit()
            flash("Patient deleted successfully!", "success")
        else:
            flash("Patient not found or unauthorized action.", "danger")
        return redirect(url_for('list_patients'))
    return render_template('delete.html', form=form)

@app.route('/medical_records/<int:patient_id>')
@login_required
def medical_records(patient_id):
    patient = Patient.query.filter_by(id=patient_id, doctor_id=current_user.id).first()
    if not patient:
        flash("Unauthorized access or patient not found.", "danger")
        return redirect(url_for('list_patients'))
    
    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
    return render_template('medical_records.html', patient=patient, medical_records=records)

@app.route('/add_record/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def add_record(patient_id):
    patient = Patient.query.filter_by(id=patient_id, doctor_id=current_user.id).first()
    if not patient:
        flash("Unauthorized access or patient not found.", "danger")
        return redirect(url_for('list_patients'))
    
    if request.method == 'POST':
        # Get the values from the form
        medications = request.form.get('medications')
        allergies = request.form.get('allergies')
        vital_signs = request.form.get('vital_signs')
        diagnosis = request.form.get('diagnosis')
        treatment_plan = request.form.get('treatment')
        description = request.form.get('description')  # Capture description field
        
        # Create a new MedicalRecord object and save it to the database
        new_record = MedicalRecord(
            patient_id=patient_id,
            medications=medications,
            allergies=allergies,
            vital_signs=vital_signs,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            description=description  # Store description
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        flash("Medical record added successfully!", "success")
        return redirect(url_for('medical_records', patient_id=patient_id))
    
    return render_template('add_record.html', patient=patient)



@app.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    
    # Ensure the record belongs to the logged-in doctor's patient
    if record.patient.doctor_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('list_patients'))
    
    if request.method == 'POST':
        # Update the record with the form data
        record.medications = request.form.get('medications')
        record.allergies = request.form.get('allergies')
        record.vital_signs = request.form.get('vital_signs')
        record.diagnosis = request.form.get('diagnosis')
        record.treatment_plan = request.form.get('treatment')
        record.description = request.form.get('description')  # Capture description
        
        db.session.commit()
        flash("Medical record updated successfully!", "success")
        return redirect(url_for('medical_records', patient_id=record.patient_id))
    
    return render_template('edit_record.html', record=record)

@app.route('/view_record/<int:record_id>')
@login_required
def view_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)

    if record.patient.doctor_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('list_patients'))

    return render_template('view_record.html', record=record)



@app.route('/confirm_delete_record/<int:record_id>', methods=['GET'])
@login_required
def confirm_delete_record_page(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    if record.patient.doctor_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('list_patients'))
    
    return render_template('delete_record.html', record=record)

@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    if record.patient.doctor_id != current_user.id:
        flash("Unauthorized action or record not found.", "danger")
        return redirect(url_for('list_patients'))
    
    db.session.delete(record)
    db.session.commit()
    flash("Medical record deleted successfully.", "success")
    return redirect(url_for('medical_records', patient_id=record.patient_id))

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
