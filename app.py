#import libraries

from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from random import seed
import random
from random import randint
import dlib,cv2
import face_recognition
import numpy as np
import os
import hashlib
from flask.helpers import flash, get_flashed_messages, send_from_directory
from datetime import timedelta
# seed random number generator
seed(1)
# generate some integers

#end


#intialise direectories and keys

UPLOAD_FOLDER = './uploads'
UPLOAD_VIDEO = './video'
DOWNLOAD = './result'
THIRDVIDEO = './third_video'
IDPROOF_FOLDER = './ID_Proof'
CRIMINAL_ID = './static/criminals'

ALLOWEDID_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
ALLOWED_FILEEXTENSIONS = set(['jpg','jpeg'])
ALLOWED_VIDEOEXTENSIONS = set(['mp4'])

app = Flask(__name__)
mail=Mail(app)
posta=Mail(app)
s = URLSafeTimedSerializer('secret')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_VIDEO'] = UPLOAD_VIDEO
app.config['DOWNLOAD'] = DOWNLOAD
app.config['THIRDVIDEO'] = THIRDVIDEO
app.config['IDPROOF_FOLDER'] = IDPROOF_FOLDER
app.config['CRIMINAL_ID'] = CRIMINAL_ID

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'secret'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pinpoint.four.2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'Google2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = "hello"

#end

#import ML models 
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
#end

#database models
db = SQLAlchemy(app)
#db is the refrence

#User table
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(50),unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(100),nullable=False)
    mail = db.Column(db.String(50))
    hash= db.Column(db.String(120))
    type = db.Column(db.String(15),nullable=False)

    def __init__(self,username,password,mail,hash,type):
        self.username=username
        self.password=password
        self.mail=mail
        self.hash=hash
        self.type=type
    
#Admin Table
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    admin_id = db.Column(db.String(20))
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)

    def __init__(self,usr_name,fname,lname,phone,admin_id):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.admin_id=admin_id 
        
#Authority Table
class Authority(db.Model):
    __tablename__ = 'Authority'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    job = db.Column(db.String(50))
    proof=db.Column(db.String(40))
    confirm=db.Column(db.Boolean,unique=False, default=False)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,usr_name,fname,lname,phone,job,proof,confirm):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.job=job
        self.proof=proof 
        self.confirm=confirm


#Ordinary Table
class Ordinary(db.Model):
    __tablename__ = 'Ordinary'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    phone = db.Column(db.Integer)
    state = db.Column(db.String(30))
    city = db.Column(db.String(30))
    proof=db.Column(db.String(40))
    address=db.Column(db.String(50))
    zip = db.Column(db.Integer)
    reason=db.Column(db.String(150))
    confirm=db.Column(db.Boolean,unique=False, default=False)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,usr_name,fname,lname,phone,state,city,address,reason,zip,proof,confirm):
        self.usr_name=usr_name
        self.fname=fname
        self.lname=lname
        self.phone=phone
        self.state=state
        self.proof=proof    
        self.address=address
        self.city=city
        self.zip=zip
        self.reason=reason
        self.confirm=confirm


#Other Table
class Other(db.Model):
    __tablename__ = 'Other'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    admin_approval = db.Column(db.String(5))
    admin_id =  db.Column(db.String(20))
    no_video_upload = db.Column(db.Integer)
    no_of_video_request = db.Column(db.Integer)
    third_party_issue_id = db.Column(db.String(20)) 
    third_party_pending_order = db.Column(db.String(10))
    third_party_response = db.Column(db.String(50))  #video available or not
    date= db.Column(db.String(20))
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    live_recording_no=db.Column(db.Integer)
    result_time = db.Column(db.String(20))
    result_query = db.Column(db.String(20))
    result_percent = db.Column(db.Integer)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)
    

    def __init__(self,admin_approval,admin_id,no_video_upload,no_of_video_request,third_party_issue_id,
    third_party_pending_order,third_party_response,date,start_time,end_time,live_recording_no,result_time,
    result_query,result_percent,usr_name):
        self.admin_approval=admin_approval
        self.admin_id=admin_id
        self.no_video_upload=no_video_upload
        self.no_of_video_request=no_of_video_request
        self.third_party_issue_id=third_party_issue_id
        self.third_party_pending_order=third_party_pending_order
        self.third_party_response=third_party_response
        self.date=date    
        self.start_time=start_time
        self.end_time=end_time
        self.live_recording_no=live_recording_no
        self.usr_name=usr_name
        self.result_time = result_time
        self.result_query = result_query
        self.result_percent = result_percent


#Third table
class Third(db.Model):
    __tablename__ = 'Third'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dept = db.Column(db.String(50))
    name = db.Column(db.String(50))
    third_party_id = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    usr_name = db.Column(db.String, db.ForeignKey('User.username'),nullable=False)

    def __init__(self,usr_name,dept,name,third_party_id,phone):
        self.usr_name=usr_name
        self.dept=dept
        self.name=name
        self.phone=phone
        self.third_party_id=third_party_id



#Count table
class Count(db.Model):
    __tablename__ = 'Count'
    id = db.Column(db.Integer, primary_key=True)
    Ordinary = db.Column(db.Integer)
    Authority = db.Column(db.Integer)
    Admin = db.Column(db.Integer)
    Third_party = db.Column(db.Integer)
    Total_Real= db.Column(db.Integer)
    Total_upload = db.Column(db.Integer)
    Total_request = db.Column(db.Integer)
    Total_crowd = db.Column(db.Integer)
    Threshhold = db.Column(db.Integer)

    def __init__(self,id,Ordinary,Authority,Admin,Third_party,Total_Real,Total_upload,Total_request,Total_crowd,Threshhold):
        self.id = id
        self.Ordinary = Ordinary
        self.Authority = Authority
        self.Admin = Admin
        self.Third_party = Third_party
        self.Total_Real = Total_Real
        self.Total_upload = Total_upload
        self.Total_request = Total_request
        self.Total_crowd = Total_crowd
        self.Threshhold = Threshhold
      

#Criminal table
class Criminals(db.Model):
    __tablename__ = 'Criminals'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    third_party_id = db.Column(db.String(20))
    url = db.Column(db.String(30))


    def __init__(self, name, age, url, third_party_id):
        self.name = name
        self.age = age
        self.url = url
        self.third_party_id = third_party_id


#end

def THreshhold():

    count = Count.query.filter(Count.id == 1).first()
    de = count.Threshhold
    return de


class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 



#ML Functions

# findface function


def find_faces(image):

    dets = detector(image, 1)
    if len(dets) == 0:
        return np.empty(0)

    shapes = []
    for k, d in enumerate(dets):
        
        shape = sp(image, d)
        shapes.append(shape)
        
    return shapes
#end

# encode face function
def encode_faces(img, shapes):
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)


writer = None


#end of class face_reco
# convert to time format
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds) 
#end

#allowed files
def allowed_file1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILEEXTENSIONS
#end

#allowed videos
def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEOEXTENSIONS
#end

#allowed IDs
def allowed_file3(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWEDID_EXTENSIONS

#end
#end

#contollers
#INdex page


@app.route('/')
def index():

    value = Count.query.filter_by(id = 1).first()
    #return '<html><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"><center><div class="card text-white bg-info" style="max-width: 80em;"><div class="card-header"><h1>Please Confirm Your Email Address</h1></div><div class="card-body"><br><p class="card-text">We have sent an email with a confirmation link to your email address. In order to complete the sign-up process, please click the confirmation link.<br><br>If you do not receive a confirmation email, please check your spam folder. Also, please verify that you entered a valid email address in our sign-up form.</p><br><br></div> </div><br><br><div class="card text-white bg-info" style="max-width: 80em;"><div class="card-header"><br><h4>Your Documents are sent to admin for Verification.After verification your account will be activated.<BR> Please wait for the account activation mail</h4></p><br><br></div></html>'
    return render_template('index.html',value = value)

@app.route('/error')
def error():

    value = Count.query.filter_by(id = 1).first()
    return render_template('index.html',scroll='re',value = value)


@app.route('/relogin')
def relogin():

    value = Count.query.filter_by(id = 1).first()
    return render_template('index.html',scroll='relogin',value = value)
    

@app.route('/user/mail/activation')
def mailactivation():
    
    return '<html><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"><center><div class="card text-white bg-info" style="max-width: 80em;"><div class="card-header"><h1>Please Confirm Your Email Address</h1></div><div class="card-body"><br><p class="card-text">We have sent an email with a confirmation link to your email address. In order to complete the sign-up process, please click the confirmation link.<br><br>If you do not receive a confirmation email, please check your spam folder. Also, please verify that you entered a valid email address in our sign-up form.</p><br><br></div> </div><br><br><div class="card text-white bg-info" style="max-width: 80em;"><div class="card-header"><br><h4>Your Documents are sent to admin for Verification.After verification your account will be activated.<BR> Please wait for the account activation mail</h4></p><br><br></div></html>'


@app.route('/register', methods=['GET','POST'])
def Register():
     if request.method == 'POST':
         fname = request.form['firstname']
         lname = request.form['lastname']
         username = request.form['username']
         password = request.form['password']
         confpassword = request.form['confpassword']
         phone = request.form['mobile']
         email = request.form['mail']
         address = request.form['address']
         state = request.form.get('state')
         city = request.form.get('city')
         reason = request.form['reason']
         zip = request.form['zipcode']
         file1 = request.files['idproof']
         proof = file1.filename
         exists = User.query.filter_by(username=username).first()
         emailid = User.query.filter_by(mail=email).first()
         if not exists and not emailid:

            if(password == confpassword):
                h = hashlib.md5(password.encode())
                enpassword = h.hexdigest()
                reg = User(username = username,password = enpassword, mail = email,hash='', type = 'Ordinary')
                db.session.add(reg)

                if file1 and allowed_file3(file1.filename):
                    filename = secure_filename(file1.filename)
                    filename = username +'_'+ filename 
                    file1.save(os.path.join(app.config['IDPROOF_FOLDER'], filename))

                ord = Ordinary(fname = fname, lname = lname, phone = phone, state = state,
                city = city,proof = filename, address = address, zip = zip, reason = reason, usr_name = username,confirm=0)
                db.session.add(ord)

                other = Other(admin_approval = 'no', admin_id = '', no_video_upload = 0, no_of_video_request = 0, 
                third_party_issue_id = '',third_party_pending_order = '',third_party_response = '', date = '', 
                start_time = '', end_time = '', live_recording_no = 0,result_time = '',result_query = '',
                result_percent = 0,usr_name = username )
                db.session.add(other)
                
                value = Count.query.filter_by(id = 1).first()
                value.Ordinary = value.Ordinary + 1
                db.session.add(value)

                db.session.commit()
                #confirmation mail
                token = s.dumps(email, salt='email-confirm')

                msg = Message('Confirm PINPOINT Account', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.html = render_template('base/email.html',link=link)
                mail.send(msg)
                
                return redirect(url_for('mailactivation'))
            else:
                flash('Password and Confirm password not matched','error')
                return redirect(url_for('error'))
                


         else:
            flash('Username or Email already taken,try somethig else','error')
            return redirect(url_for('error'))
             
            

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=172800)
    except SignatureExpired:
        return render_template('back.html',email2 = 1)
    use = User.query.filter_by(mail=email).first()
    if use:
        print(use.type)
        if use.type == "Ordinary":
            Ord = Ordinary.query.filter_by(usr_name=use.username).first()
            
        if use.type == "Authority":
            Ord = Authority.query.filter_by(usr_name=use.username).first()
            
        Ord.confirm = 1
        db.session.add(Ord)
        db.session.commit()
        return '<h1>Your email is verifed!</h1>'
        
    else:
        return render_template('back.html',email1 = 1)


@app.route('/reg_official', methods=['GET','POST'])
def Register2():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['uname']
        password = request.form['password']
        confpassword = request.form['confpassword']
        phone = request.form['mobile']
        email = request.form['email']
        job = request.form['job']
        department = request.form['department']
        file1 = request.files['jobproof']
        proof = file1.filename
        if job == 'Other':
            job = department
        exists = User.query.filter_by(username=username).first()
        emailid = User.query.filter_by(mail=email).first()
        if not exists and not emailid:

            if(password == confpassword):
                h = hashlib.md5(password.encode())
                enpassword = h.hexdigest()
                reg = User(username = username,password = enpassword, mail = email,hash='', type = 'Authority')
                db.session.add(reg)

                if file1 and allowed_file3(file1.filename):
                    filename = secure_filename(file1.filename)
                    filename = username +'_'+ filename 
                    file1.save(os.path.join(app.config['IDPROOF_FOLDER'], filename))

                Auth = Authority(fname = fname, lname = lname, phone = phone, proof = filename, job=job , usr_name = username,confirm=0)
                db.session.add(Auth)

                other = Other(admin_approval = 'no', admin_id = '', no_video_upload = 0, no_of_video_request = 0, 
                third_party_issue_id = '',third_party_pending_order = '',third_party_response = '', date = '', 
                start_time = '', end_time = '', live_recording_no = 0,result_time = '',result_query = '',
                result_percent = 0, usr_name = username )
                db.session.add(other)
                
                value = Count.query.filter_by(id = 1).first()
                value.Authority = value.Authority + 1
                db.session.add(value)
                
                db.session.commit()
                #confirmation mail
                token = s.dumps(email, salt='email-confirm')
                msg = Message('Confirm PINPOINT Account', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.html = render_template('base/email.html',link=link)
                mail.send(msg)
                
                return redirect(url_for('mailactivation'))
            else:
                flash('Password and Confirm password not matched','error')
                return redirect(url_for('error'))

        else:
            
            flash('Username or Email already taken,try somethig else','error')
            return redirect(url_for('error'))
        

            
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.permanent = True       
        uname = request.form['uname']
        passw = request.form['psw']
        h = hashlib.md5(passw.encode())
        enpassword = h.hexdigest()
        
        login = User.query.filter_by(username=uname, password=enpassword).first()

        if login:
            
            if login.hash == "rejected":
                return render_template('back.html',adminrej = 1)

            if login.type == 'Admin':
                session["admin"] = uname
                flash(uname + ' Successfully Logged in','mass')
                return redirect(url_for('admindashboard'))

            elif login.type == 'Ordinary' or login.type == 'Authority':
                oth = Other.query.filter_by(usr_name=uname).first()
                if login.type == 'Ordinary':
                    con = Ordinary.query.filter_by(usr_name=uname).first()
                    if con.confirm == 0:
                        return redirect(url_for('mailactivation'))
                    if oth.admin_approval == "no":
                        return render_template('base/back.html',adminver = 1)
                    if oth.admin_approval == "reject":
                        return render_template('base/back.html',adminrej = 1)
                
                if login.type == 'Authority':
                    con = Authority.query.filter_by(usr_name=uname).first()
                    if con.confirm == 0:
                        return redirect(url_for('mailactivation'))
                    if oth.admin_approval == "no":
                        return render_template('base/back.html',adminver = 1)
                    if oth.admin_approval == "reject":
                        return render_template('base/back.html',adminrej = 1)


                session["user"] = uname
                flash(uname + ' Successfully Logged in','mass')
                return redirect(url_for('current'))

            elif login.type == 'Third_party':
                session["third"] = uname
                flash(uname + ' Successfully Logged in','mass')
                return redirect(url_for('thirddashboard'))
            else: 
                return "ll"
        else:
            flash('User is Not Registerd','error')
            return redirect(url_for('relogin'))

            
#end

# Current page 

@app.route('/user/current')
def current():
  if "user" in session:
    all = db.session.query(Third.dept.distinct()).all()
    print(all)
    
    a = []
    for al in all:
        a.append(Third.query.filter_by(dept = al[0]).all())
    print(a)
    for am in a:
        print(a.index(am))
        for ah in am:
            print(ah.name)
    for al in all:
        print(all.index(al))

    id = User.query.filter_by(username = session["user"]).first()
    id2 = id.type
    email = id.mail
    print(id2)
    notifi = Other.query.filter_by(usr_name = session["user"],no_of_video_request = 2).first()
    print(notifi)
    if notifi != None:
        if(notifi.result_time == ''):
            notifi = 'not'
    if(id.type == "Ordinary"):
        pro = Ordinary.query.filter_by(usr_name = session["user"]).first()
        print(pro)

    if(id.type == "Authority"):
        pro = Authority.query.filter_by(usr_name = session["user"]).first()

    
    if all == []:
        return render_template('base/current.html',third = "third",profile=pro,id = id2,mail = email,notifi = notifi,user = session["user"])


    return render_template('base/current.html',all=all,a=a,profile=pro,id = id2, mail = email,notifi = notifi,user = session["user"])
  
  else:
      return redirect(url_for('relogin'))



@app.route('/user/output')
def output():
    if "user" in session:
        return render_template('base/output.html',user = session["user"])
    else:
      return redirect(url_for('relogin'))



@app.route('/user/update/profile', methods=['POST'])
def profileupdate():
    if "user" in session:

     if request.method == 'POST':
         typeid = request.form['id']
         email = request.form['email']
         use = User.query.filter_by(mail = email).first()
         if use:
             flash("Email ID Already in Use",'error')
             return redirect(url_for('current'))

         if typeid == "Ordinary":
             print(typeid)
             fname = request.form['fname']
             lname = request.form['lname']
             mobile = request.form['mobile']
             email = request.form['email']
             address = request.form['address']
             state = request.form['state']
             city = request.form['city']
             zip = request.form['zip']
             
            

             ordi = Ordinary.query.filter_by(usr_name = session["user"]).first()
             ordi.fname = fname
             ordi.lname = lname
             ordi.phone = mobile
             ordi.address = address
             if state != "":
                 ordi.state = state
                 ordi.city = city
             ordi.zip = zip

             user1 = User.query.filter_by(username = session["user"]).first()
             user1.mail = email

             db.session.add(user1)
             db.session.add(ordi)

             db.session.commit()
             flash("Successfully Updated Your Profile",'success')
             return redirect(url_for('current'))

            


         elif typeid == "Authority":
             print(typeid)
             fname = request.form['fname']
             lname = request.form['lname']
             mobile = request.form['mobile']
             email = request.form['email']
             job = request.form['job']
             department = request.form['department']
             

             auth = Authority.query.filter_by(usr_name = session["user"]).first()
             auth.fname = fname
             auth.lname = lname
             auth.phone = mobile
             
             if job != "":
                if job == "Other":
                    job = department
                    auth.job = job
                else:
                    auth.job = job
            
             user1 = User.query.filter_by(username = session["user"]).first()
             user1.mail = email

             db.session.add(user1)
             db.session.add(auth)

             db.session.commit()
             flash("Successfully Updated Your Profile",'success')
             return redirect(url_for('current'))         


         return typeid
    else:
      return redirect(url_for('relogin'))



@app.route('/user/update/password', methods=['POST'])
def passwordupdate():

  if "user" in session:

     if request.method == 'POST':
        currentpass = request.form['psw1']
        newpassword = request.form['psw2']
        confpassword = request.form['psw3']

        if newpassword == confpassword:
            h = hashlib.md5(currentpass.encode())
            enpassword = h.hexdigest()
            user = User.query.filter_by(username = session["user"],password = enpassword).first()
            if user:
                h = hashlib.md5(newpassword.encode())
                enpassword = h.hexdigest()
                if user.password == enpassword:
                    flash("You have Entered same Password, Try some other",'error')
                else:
                    user.password = enpassword
                    db.session.add(user)
                    db.session.commit()
                    flash("Successfully Changed Password",'success')
            else:
                flash("You Entered Wrong Password",'error')

        else:
            flash("New password is not matching",'error')
        
        return redirect(url_for('current'))
  
  else:
      return redirect(url_for('relogin'))



@app.route('/user/update/username', methods=['POST'])
def usernameupdate():

  if "user" in session:

    if request.method == 'POST':
        currentuser = request.form['username1']
        newuser = request.form['username2']
        confuser = request.form['username3']

        if newuser == confuser:
          if currentuser == session["user"]:
            user = User.query.filter_by(username = currentuser).first()
            if user:
              if User.query.filter_by(username = newuser).first():
                  flash("New Username Already exist, Try some other",'error')
                  return redirect(url_for('current'))
              else:
                if user.username == newuser:
                    flash("You have Entered same Username, Try some other",'error')
                    return redirect(url_for('current'))
                else:
                    if user.type == "Ordinary":
                        ord = Ordinary.query.filter_by(usr_name = currentuser).first()
                        oth = Other.query.filter_by(usr_name = currentuser).first()
                        ord.usr_name = newuser
                        oth.usr_name = newuser
                        user.username = newuser
                        db.session.add(user)
                        db.session.add(ord)
                        db.session.add(oth)
                        db.session.commit()
                        session["user"] = newuser
                    
                    if user.type == "Authority":
                        auth = Authority.query.filter_by(usr_name = currentuser).first()
                        oth = Other.query.filter_by(usr_name = currentuser).first()
                        auth.usr_name = newuser
                        oth.usr_name = newuser
                        user.username = newuser
                        db.session.add(user)
                        db.session.add(auth)
                        db.session.add(oth)
                        db.session.commit()
                        session["user"] = newuser
                    
                    
                    flash("Successfully Changed Username",'success')
                    return redirect(url_for('current'))
            else:
                flash("You Entered Wrong Username",'error')
                return redirect(url_for('current'))
          else:
              flash("You Entered Wrong Username",'error')
              return redirect(url_for('current'))

        else:
            flash("New Username is not matching",'error')
            return redirect(url_for('current'))

  else:
      return redirect(url_for('relogin'))      
        
    

@app.route('/user/deleteaccount', methods=['POST'])
def delete():

  if "user" in session:

    if request.method == 'POST':
        password = request.form['password']
        h = hashlib.md5(password.encode())
        enpassword = h.hexdigest()
        user = User.query.filter_by(username = session["user"],password = enpassword ).first()
        if user:
            delete1 = db.session.query(User).filter(User.username == session["user"]).first()

            if user.type == "Ordinary":
                delete2 = Ordinary.query.filter(Ordinary.usr_name == session["user"]).first()
                delete3 = Other.query.filter(Other.usr_name == session["user"]).first()
                count = Count.query.filter(Count.id == 1).first()
                count.Ordinary = count.Ordinary -1

            elif user.type == "Authority":
                delete2 = Authority.query.filter(Authority.usr_name == session["user"]).first()
                delete3 = Other.query.filter(Other.usr_name == session["user"]).first()
                count = Count.query.filter(Count.id == 1).first()
                count.Ordinary = count.Ordinary -1
        
            db.session.add(count)
            db.session.delete(delete1)
            db.session.delete(delete2)
            db.session.delete(delete3)
            db.session.commit()

            session.clear()

            flash("You have Successfully Deleted Your Account",'success')
            return redirect(url_for('index'))
        
        else: 
            flash("You have entered Wrong Password",'error')
            return redirect(url_for('current'))

        return ""
  else:
      return redirect(url_for('relogin'))



@app.route('/user/result/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if "user" in session:
        return send_from_directory(directory='static/result', filename=filename)
    else:
      return redirect(url_for('relogin'))



@app.route('/user/upload', methods=['POST'])
def train():
    
  if "user" in session:

    filelist = [f for f in os.listdir('uploads/')]
    for f in filelist:
        os.remove(os.path.join('uploads/', f))
    
    
    if request.method == 'POST':
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if f and allowed_file1(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash("Invalid Input File Format; only jpeg or jpg supported",'error')
                print("Invalid Input File Format; only jpeg or jpg supported")
                return redirect(url_for('current'))
        
        myimages = []
        dirfiles = os.listdir('uploads/')
        sorted(dirfiles)
        for files in dirfiles:
            if '.jpg' in files:
                myimages.append(files)
            if '.jpeg' in files:
                myimages.append(files)
        no_of_images = len(myimages)
        if no_of_images > 2:
            flash('Maximum Number of Images is 2','error')
            print("Maximum Number of Images is 2 ")
            filelist = [f for f in os.listdir('uploads/')]
            for f in filelist:
                os.remove(os.path.join('uploads/', f))
            return redirect(url_for('current'))


        names = [x[:-4] for x in myimages]
        paths = ['uploads/' + x for x in myimages]
        print(names) 
    
        descs = {}

        for i in range(0,no_of_images):    
            img_bgr = cv2.imread(paths[i])
            image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            if len(detector(image, 1)) == 0 :
                flash('Please change image: ' + myimages[i] + ' - it has No faces','error')
                print("Please change image: " + myimages[i] + " - it has No faces; atleast one face needed")
                return redirect(url_for('current'))

            if len(detector(image, 1)) > 1 :
                flash('Please change image: ' + myimages[i] + ' - it has ' + str(len(detector(image, 1))) + " faces",'error')
                print("Please change image: " + myimages[i] + " - it has " + str(len(detector(image, 1))) + " faces; it can only have one")
                return redirect(url_for('current'))

            img_shapes = find_faces(image)
            descs[i] = encode_faces(image, img_shapes)[0]
        if request.form['action'] == 'Request_Video':

            check = Other.query.filter_by(usr_name = session["user"]).first()
            if check.no_of_video_request == 1:
                flash('You have already request for one video so you cannot Request anymore','error')
                print("You have already request for one video so you cannot Request anymore")
                return redirect(url_for('current'))
            if check.no_of_video_request == 2:
                flash('Please check your Notification;Then only we will consider your next request','error')
                print("Please check your Notification;Then only we will consider your next request")
                return redirect(url_for('current'))


            np.save('third_image/'+ session["user"]+ '.npy', descs)

            dept = request.form['firstList']
            name = request.form['secondList'+ dept]
            date = request.form.get('date')
            start_time = request.form.get('starttime')
            end_time = request.form.get('endtime')


            print(dept)
            print(name)
            print(date)
            print(start_time)
            print(end_time)

            fish = db.session.query(Third.dept.distinct()).all()
            print(fish[int(dept)][0])
            depta = fish[int(dept)][0]

            mass = Third.query.filter_by(dept = depta, name = name).first()
            print(mass.third_party_id)
            ID = mass.third_party_id
            
            send = Other.query.filter_by(usr_name = session["user"]).first()
            send.third_party_issue_id = ID
            send.third_party_pending_order = 'no'
            send.third_party_response = ''
            send.date = date
            send.start_time = start_time
            send.end_time = end_time
            send.no_of_video_request = 1

            db.session.add(send)
            db.session.commit()
            flash("You have successfully submit your request. Please  Wait for the notification Mail ")
            return render_template('base/output.html' ,output = 1, user = session["user"])




           
        elif request.form['action'] == "Upload":
            
            videos = request.files.getlist("videos")
            f = videos[0]
            if len(videos) == 1 :
                    if not allowed_file2(f.filename):
                        flash('Invalid Video Format ;Only Mp4 Supported','error')
                        print("Invalid Video Format ;Only Mp4 Supported")
                        return redirect(url_for('current'))
                    f.filename = session["user"] + ".mp4"
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_VIDEO'], filename))
                    video_path = 'video/'+ f.filename
                    print(video_path)
                    cap = cv2.VideoCapture(video_path)
                    if not cap.isOpened():
                        flash('Video cannot Open','error')
                        print("Video cannot Open")
                        return redirect(url_for('current'))
        
                    _, img_bgr = cap.read()
                    padding_size = 0
                    resized_width = 2000
                    video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
                    output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

                    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                    writer = cv2.VideoWriter('static/result/'+session["user"]+'.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS),output_size)
                    m=-1
                    i=1
                    s=0
                    c=1
                    th = THreshhold()
                    while True:
                        
                        ret, img_bgr = cap.read()
                        if not ret:
                            break
    
                        img_bgr = cv2.resize(img_bgr, video_size)
                        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                        dets = detector(img_bgr, 1)

                        for k, d in enumerate(dets):
                            shape = sp(img_rgb, d)
                            face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

                            last_found = {'name': 'unknown', 'dist': th, 'color': (0,0,255), 'percent': 0}

                            for name, saved_desc in descs.items():
                                dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                                if dist < last_found['dist']:
                                    perce =(1-dist)*100
                                    last_found = {'name': "Target", 'dist': dist, 'color': (255,255,255), 'percent': perce}
                                    if dist< c:
                                        c=dist
                                    if m == -1:
                                        s = i
                                        m=0
                                    
                            cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
                            cv2.putText(img_bgr, last_found['name'] + " (" + str(last_found['percent']) + "%)" , org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=last_found['color'], thickness=2)
                        i=i+1
                        writer.write(img_bgr)
                    
                
                    cap.release()
                    writer.release()
                    time = convert(s/24)
                    maxacc = (1-c)*100
                    print(maxacc)
                    print(convert(s/24)) 
                    success = "You have successfully Processed the Video"

                    send = Other.query.filter_by(usr_name = session["user"]).first()
                    send.no_video_upload = send.no_video_upload + 1
                    db.session.add(send)

                    count = Count.query.filter_by(id = 1).first()
                    count.Total_upload = count.Total_upload + 1
                    db.session.add(count)

                    db.session.commit()
                    return render_template('base/output.html',success = success,maxacc=maxacc, time = time,s=s,user = session["user"] )

            else:
                flash('Only one video can upload','error')
                print("Only one video can upload")
                return redirect(url_for('current'))



        elif request.form['action'] == "ON":
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                flash('Camera is not working','error')
                print("Camera is not working")
                return redirect(url_for('current'))
        
            _, img_bgr = cap.read()
            padding_size = 0
            resized_width = 2000
            video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
            output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            writer = cv2.VideoWriter('static/result/'+session["user"]+'.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
            m=-1
            i=1
            s=0
            c=1
            th = THreshhold()
            while True:
                        
                ret, img_bgr = cap.read()
                if not ret:
                    break

                img_bgr = cv2.resize(img_bgr, video_size)
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                dets = detector(img_bgr, 1)

                for k, d in enumerate(dets):
                    shape = sp(img_rgb, d)
                    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

                    last_found = {'name': 'unknown', 'dist': th, 'color': (0,0,255),'percent': 0}

                    for name, saved_desc in descs.items():
                        dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                        if dist < last_found['dist']:
                            perce = (1-dist)*100
                            last_found = {'name': "Target", 'dist': dist, 'color': (255,255,255), 'percent': perce}
                            if dist< c:
                                c=dist
                            if m == -1:
                                s = i
                                m=0
                                    
                    cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
                    cv2.putText(img_bgr, last_found['name'] + " (" + str(last_found['percent']) + "%)" , org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=last_found['color'], thickness=2)
                i=i+1
                writer.write(img_bgr)
                cv2.imshow('img', img_bgr)
                if cv2.waitKey(1) == ord('q'):
                    break
                    
                
            cap.release()
            writer.release()
            maxacc = (1-c)*100
            print(maxacc)
            time = convert(s/24)
            print(convert(s/24)) 
            success = "You have successfully Processed the Video"

            send = Other.query.filter_by(usr_name = session["user"]).first()
            send.live_recording_no = send.live_recording_no + 1
            db.session.add(send)

            count = Count.query.filter_by(id = 1).first()
            count.Total_Real = count.Total_Real + 1
            db.session.add(count)

            db.session.commit()
            return render_template('base/output.html',success = success, time = time,maxacc =maxacc, s=s,user = session["user"])
        
    else:
        print("Error")
        exit()
  else:
      return redirect(url_for('relogin'))

@app.route('/user/Processed/none', methods=['GET', 'POST'])
def clickback():
    if "user" in session:
        send = Other.query.filter_by(usr_name = session["user"]).first()
        send.no_of_video_request = 0
        db.session.add(send)
        db.session.commit()

        return redirect(url_for('current'))

    else:
      return redirect(url_for('relogin'))



@app.route('/user/Processed/result/<path:filename>', methods=['GET', 'POST'])
def download5(filename):
    if "user" in session:

        send = Other.query.filter_by(usr_name = session["user"]).first()
        send.no_of_video_request = 0
        send.result_time = ''
        send.result_percent = ''
        send.result_query = ''
        db.session.add(send)
        db.session.commit()

        return send_from_directory(directory='static/result', filename=filename)
    else:
      return redirect(url_for('relogin'))

#end


#Thirdparty Page

@app.route('/thirdparty')
def  thirddashboard():

  if "third" in session:
    
    all = Other.query.filter_by(third_party_issue_id = session["third"],third_party_pending_order = 'no').all()
    criminals = (db.session.query(Criminals).filter(Criminals.third_party_id == Third.third_party_id).join(Third,Third.usr_name == session["third"])).all()
    len1 = len(all)
    print(criminals)
    third = Third.query.filter_by(usr_name = session["third"]).first()
    user1 = User.query.filter_by(username = session["third"]).first()
    email = user1.mail
    if (len1 == 0):
        value = 'None'
        flash("You do not have any Request",'None')
        return render_template('third/thirdparty.html',all=all,value = value,user=session["third"],third = third,email=email,criminals = criminals)

    else:
        value = 'success'
        flash("You Have " + str(len1) + " Request",'success5')
        return render_template('third/thirdparty.html',all=all,value = value,user=session["third"],third=third,email=email,criminals = criminals)
    
  else:
      return redirect(url_for('relogin'))



@app.route('/thirdparty/editprofile', methods=["POST"])
def editthird():
 if "third" in session:

    email = request.form['email']
    use = User.query.filter_by(mail = email).first()
    if use:
        flash("Email ID Already in Use",'error')
        return redirect(url_for('thirddashboard'))


    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        print(name)
        print(email)
        print(phone)

        third = Third.query.filter_by(usr_name = session["third"]).first()
        print(third)
        third.name = name
        third.phone = phone

        user1 = User.query.filter_by(username = session["third"]).first()
        user1.mail = email

        db.session.add(user1)
        db.session.add(third)

        db.session.commit()
        flash("You have successfully updated your profile",'success')
    return redirect(url_for('thirddashboard'))
 else:

    return redirect(url_for('relogin'))



@app.route('/thirdparty/updatepassword', methods=["POST"])
def updatethirdpass():
    if "third" in session:

        if request.method == 'POST':
            currentpass = request.form['oldpass']
            newpassword = request.form['newpass']
            confpassword = request.form['confpass']

            if newpassword == confpassword:
                h = hashlib.md5(currentpass.encode())
                enpassword = h.hexdigest()
                user = User.query.filter_by(username = session["third"],password = enpassword).first()
                if user:
                    h = hashlib.md5(newpassword.encode())
                    enpassword = h.hexdigest()
                    if user.password == enpassword:
                        flash("You have Entered same Password, Try some other",'error')
                    else:
                        user.password = enpassword
                        db.session.add(user)
                        db.session.commit()
                        flash("Successfully Changed Password",'success')
                else:
                    flash("You Entered Wrong Password",'error')

            else:
                flash("New password is not matching",'error')
        
            return redirect(url_for('thirddashboard'))
  
    else:
        return redirect(url_for('relogin'))



@app.route('/thirdparty/editusername', methods=["POST"])
def edituserthird():

    if "third" in session:

        if request.method == 'POST':
            currentuser = request.form['olduser']
            newuser = request.form['newuser']
            confuser = request.form['confuser']

            if newuser == confuser:
                if currentuser == session["third"]:
                    user = User.query.filter_by(username = currentuser).first()
                    if user:
                        if User.query.filter_by(username = newuser).first():
                            flash("New Username Already exist, Try some other",'error')
                            return redirect(url_for('thirddashboard'))
                        else:
                            if user.username == newuser:
                                flash("You have Entered same Username, Try some other",'error')
                                return redirect(url_for('thirddashboard'))
                            else:
                                if user.type == "Third_party":
                                    th = Third.query.filter_by(usr_name = currentuser).first()
                                    th.usr_name = newuser
                                    user.username = newuser
                                    db.session.add(user)
                                    db.session.add(th)
                                    db.session.commit()
                                    session["third"] = newuser
                    
                                    flash("Successfully Changed Username",'success')
                                    return redirect(url_for('thirddashboard'))
                    else:
                        flash("You Entered Wrong Username",'error')
                        return redirect(url_for('thirddashboard'))
                else:
                    flash("You Entered Wrong Username",'error')
                    return redirect(url_for('thirddashboard'))

            else:
                flash("New Username is not Matching",'error')
                return redirect(url_for('thirddashboard'))

    else:
        return redirect(url_for('relogin'))      



@app.route('/thirdparty/delete', methods=['POST'])
def deletethird():

  if "third" in session:

    if request.method == 'POST':
        password = request.form['password']
        h = hashlib.md5(password.encode())
        enpassword = h.hexdigest()
        user = User.query.filter_by(username = session["third"],password = enpassword ).first()
        if user:
            delete1 = db.session.query(User).filter(User.username == session["third"]).first()

            if user.type == "Third_party":
                delete2 = Third.query.filter(Third.usr_name == session["third"]).first()
                count = Count.query.filter(Count.id == 1).first()
                count.Third_party = count.Third_party - 1
        
                db.session.add(count)
                db.session.delete(delete1)
                db.session.delete(delete2)
                db.session.commit()

                session.clear()   
                return redirect(url_for('index'))
        
        else: 
            flash("You have Entered Wrong Password",'error')
            return redirect(url_for('thirddashboard'))

        return ""
  else:
      return redirect(url_for('relogin'))




@app.route('/thirdparty/addcriminal',methods=['POST'])
def  AddCriminal():

    if "third" in session:

        if request.method == 'POST':

            file = request.files['inputcriminal']
            name = request.form['name']
            age = request.form['age']

            if allowed_file1(file.filename):
                filename = name + '_' + file.filename
                file.save(os.path.join(app.config['CRIMINAL_ID'], filename))
            else:
                flash("Invalid Input File Format; only jpeg or jpg supported",'error')
                print("Invalid Input File Format; only jpeg or jpg supported")
                return redirect(url_for('thirddashboard'))

            third = Third.query.filter_by(usr_name = session["third"]).first()
            thirdpartyid = third.third_party_id

            use = Criminals(name = name, age = age, url = filename, third_party_id = thirdpartyid)
            db.session.add(use)
            db.session.commit() 

            flash("Successfully Saved",'success')
            return redirect(url_for('thirddashboard'))
 
    else:
      return redirect(url_for('relogin'))



@app.route('/thirdparty/deletecriminal/<path:id>')

def  DeleteCriminal(id):

    if "third" in session:
        delete1 = db.session.query(Criminals).filter(Criminals.id == id).first()
        ff = Criminals.query.filter_by(id = id).first()
        f = ff.url
        os.remove(os.path.join('static/criminals/', f))
        db.session.delete(delete1)
        db.session.commit()
        flash("You have successfully Delete the Criminal",'success')
        return redirect(url_for('thirddashboard'))
        
    else:
      return redirect(url_for('relogin'))


@app.route('/thirdparty/criminalchecking',methods=['POST'])
def CriminalChecking():

    if "third" in session:

        if request.method == 'POST':

            if request.form['action'] == "upload":

                file = request.files['video']
                if not allowed_file2(file.filename):
                    flash('Invalid Video Format ;Only Mp4 Supported','errorvideo')
                    print("Invalid Video Format ;Only Mp4 Supported")
                    return redirect(url_for('thirddashboard'))
                file.filename = session["third"] + ".mp4"
                print(file.filename)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_VIDEO'], filename))
                video_path = 'video/'+ file.filename
                print(video_path)

            if request.form['action'] == "real":

                video_path = 0
                
            third = Third.query.filter_by(usr_name = session["third"]).first()
            thirdpartyid = third.third_party_id

            crimini = Criminals.query.filter_by(third_party_id = thirdpartyid).all()
            print(len(crimini))

            img_paths = my_dictionary() 
            descs = my_dictionary()

            for user in crimini:
                img_paths.add(user.name,'static/criminals/'+ user.url)
                descs.add(user.name, None)
            
            print(img_paths)
            print(descs)

            for name, img_path in img_paths.items():
                img_bgr = cv2.imread(img_path)
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                img_shapes = find_faces(img_rgb)
                descs[name] = encode_faces(img_rgb, img_shapes)[0]
            
            print(descs)
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                flash('Camera is not working','errorcamera')
                print("Camera is not working")
                return redirect(url_for('thirddashboard'))
        
            _, img_bgr = cap.read()
            padding_size = 0
            resized_width = 500
            video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
            output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            writer = cv2.VideoWriter('static/result/'+session["third"]+'.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
       
            th = THreshhold()
            while True:
                        
                ret, img_bgr = cap.read()
                if not ret:
                    break

                img_bgr = cv2.resize(img_bgr, video_size)
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                dets = detector(img_bgr, 1)

                for k, d in enumerate(dets):
                    shape = sp(img_rgb, d)
                    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

                    last_found = {'name': 'unknown', 'dist': th, 'color': (0,0,255),'percent': 0}

                    for name, saved_desc in descs.items():
                        dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                        if dist < last_found['dist']:
                            perce = (1-dist)*100
                            last_found = {'name': name, 'dist': dist, 'color': (255,255,255), 'percent': perce}
                            
                                    
                    cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
                    cv2.putText(img_bgr, last_found['name'] + " (" + str(last_found['percent']) + "%)" , org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=last_found['color'], thickness=3)

                writer.write(img_bgr)
                if request.form['action'] == "real":
                    cv2.imshow('img', img_bgr)
                    if cv2.waitKey(1) == ord('q'):
                        break
                    
                
            cap.release()
            writer.release()

            flash('Successfully Processed video','successcriminal')
            return redirect(url_for('thirddashboard'))

        
    else:
      return redirect(url_for('relogin'))

@app.route('/thirdparty/result/criminal')
def criminaldownload():
    if "third" in session:
        return send_from_directory(directory='static/result', filename=session["third"] + '.mp4')
    else:
      return redirect(url_for('relogin'))



@app.route('/thirdparty/pendinguser',methods=['POST'])
def  PendingUser():

    if "third" in session:

        if request.method == 'POST':

            file = request.files['video']
            userid = request.form['userid']
            username = request.form['username']
            response = request.form['response']
            print(file.filename)
            print(username)
            if request.form['accept'] == "accept":

                    if not allowed_file2(file.filename):
                        flash('Invalid Video Format ;Only Mp4 Supported','errorvideo')
                        print("Invalid Video Format ;Only Mp4 Supported")
                        return redirect(url_for('thirddashboard'))
                    file.filename = username + ".mp4"
                    print(file.filename)
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['THIRDVIDEO'], filename))
                    ord = Other.query.filter_by(id = userid).first()
                    ord.third_party_pending_order = 'yes'
                    ord.third_party_response = response
                    db.session.add(ord)
                    db.session.commit()
                    flash("You have successfully submit Video",'success1')
                    return redirect(url_for('thirddashboard'))
            elif request.form['accept'] == "reject":
                    ord = Other.query.filter_by(id = userid).first()
                    ord.third_party_pending_order = 'reject'
                    ord.third_party_response = response
                    db.session.add(ord)
                    db.session.commit()
                    flash("You have successfully  Sent your Response ",'success2')
                    return redirect(url_for('thirddashboard'))

    else:
      return redirect(url_for('relogin'))

            
@app.route('/thirdparty/realtimevideo',methods=['POST'])
def  reatimevideo1():
  
  if "third" in session:

    filelist = [f for f in os.listdir('uploads/')]
    for f in filelist:
        os.remove(os.path.join('uploads/', f))

    if request.method == 'POST':
        
        uploaded_files = request.files.getlist("livefile")
        print(uploaded_files)
        for f in uploaded_files:
            if f and allowed_file1(f.filename):
                filename = secure_filename(f.filename)
                print(filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Invalid Input File Format; only jpeg or jpg supported','errorimage')
                print("Invalid Input File Format; only jpeg or jpg supported")
                return redirect(url_for('thirddashboard'))
        
        myimages = []
        dirfiles = os.listdir('uploads/')
        sorted(dirfiles)
        for files in dirfiles:
            if '.jpg' in files:
                myimages.append(files)
            if '.jpeg' in files:
                myimages.append(files)
        no_of_images = len(myimages)
        if no_of_images > 2:
            flash('Maximum Number of Images is 2','errornumber')
            print("Maximum Number of Images is 2 ")
            filelist = [f for f in os.listdir('uploads/')]
            for f in filelist:
                os.remove(os.path.join('uploads/', f))
            return redirect(url_for('thirddashboard'))


        names = [x[:-4] for x in myimages]
        paths = ['uploads/' + x for x in myimages]
        print(names) 
    
        descs = {}

        for i in range(0,no_of_images):    
            img_bgr = cv2.imread(paths[i])
            image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            if len(detector(image, 1)) == 0 :
                flash('Please change image: ' + myimages[i] + ' - it has No faces','errorface')
                print("Please change image: " + myimages[i] + " - it has No faces; atleast one face needed")
                return redirect(url_for('thirddashboard'))
            elif len(detector(image, 1)) > 1 :
                flash('Please change image: ' + myimages[i] + ' - it has ' + str(len(detector(image, 1))) + ' faces','errorface')
                print("Please change image: " + myimages[i] + " - it has " + str(len(detector(image, 1))) + " faces; it can only have one")
                return redirect(url_for('thirddashboard'))

            img_shapes = find_faces(image)
            descs[i] = encode_faces(image, img_shapes)[0]
        
            
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            flash('Camera is not working','errorcamera')
            print("Camera is not working")
            return redirect(url_for('thirddashboard'))
        
        _, img_bgr = cap.read()
        padding_size = 0
        resized_width = 2000
        video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
        output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter('static/result/'+session["third"]+'.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
        m=-1
        i=1
        s=0
        c=1
        th = THreshhold()
        while True:
                        
            ret, img_bgr = cap.read()
            if not ret:
                break

            img_bgr = cv2.resize(img_bgr, video_size)
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            dets = detector(img_bgr, 1)

            for k, d in enumerate(dets):
                shape = sp(img_rgb, d)
                face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

                last_found = {'name': 'unknown', 'dist': th, 'color': (0,0,255),'percent': 0}

                for name, saved_desc in descs.items():
                    dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                    if dist < last_found['dist']:
                        perce = (1-dist)*100
                        last_found = {'name': "Target", 'dist': dist, 'color': (255,255,255), 'percent': perce}
                        if dist< c:
                            c=dist
                        if m == -1:
                            s = i
                            m=0
                                    
                cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
                cv2.putText(img_bgr, last_found['name'] + " (" + str(last_found['percent']) + "%)" , org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=last_found['color'], thickness=2)
            i=i+1
            writer.write(img_bgr)
            cv2.imshow('img', img_bgr)
            if cv2.waitKey(1) == ord('q'):
                break
                    
                
        cap.release()
        writer.release()
        maxacc = (1-c)*100
        print(maxacc)
        time = convert(s/24)
        print(convert(s/24)) 


        count = Count.query.filter_by(id = 1).first()
        count.Total_Real = count.Total_Real + 1
        db.session.add(count)
        db.session.commit()

        flash("You have successfully Processed the Video",'success3')
        return redirect(url_for('thirddashboard'))

    else:
        print("Error")
        exit()
  else:
      return redirect(url_for('relogin'))



@app.route('/thirdparty/crowdcount',methods=['POST'])
def crowdcount():
    if "third" in session:
        if request.method == 'POST':

            limit = request.form['limit']
            if request.form['action'] == "upload":

                file = request.files['inputvideo']
                if not allowed_file2(file.filename):
                    flash('Invalid Video Format ;Only Mp4 Supported','errorvideo')
                    print("Invalid Video Format ;Only Mp4 Supported")
                    return redirect(url_for('thirddashboard'))
                file.filename = session["third"] + ".mp4"
                print(file.filename)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_VIDEO'], filename))

                video_path = 'video/'+ file.filename
                print(video_path)
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    flash('Video cannot open','errorcamera')
                    print("Video cannot open")
                    return redirect(url_for('thirddashboard'))

            if request.form['action'] == "real":
            
                video_path = 0
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    flash('Camera is not working','errorcamera')
                    print("Camera is not working")
                    return redirect(url_for('thirddashboard'))
            _, img_bgr = cap.read() 
            writer = None
            W = None
            H = None
            c=0

            if W is None or H is None:
                (H, W) = img_bgr.shape[:2]
            thresh = 0
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter('result/output.avi', fourcc, 30, (W, H), True)
            while True:

                ret, camera = cap.read()
                if not ret:
                    break
                gray = cv2.cvtColor(camera, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(gray, model='hog')
                for (top, right, bottom, left) in boxes:
                    cv2.rectangle(camera, (left, top), (right, bottom), (0, 255, 0), 2)
                writer.write(camera)
                if len(boxes) > thresh:  
                        print(len(boxes))
                        thresh = len(boxes)
                if thresh >= int(limit):
                        c = 1
                        break
                if request.form['action'] == "real":
                    cv2.imshow('img', camera)
                    if cv2.waitKey(1) == ord('q'):
                        break

            print(thresh)
            cv2.destroyAllWindows()
            cap.release()
            writer.release()
            if c == 1:
                flash('Total face count is : '+ str(thresh),'successcrowd')
                print("Total count : "+ str(thresh))
            else:
                flash('Total face count is : '+ str(thresh) + '! Not Exceeded','success')
                print("Total count : "+ str(thresh))
            return redirect(url_for('thirddashboard'))

    else:
        return redirect(url_for('relogin'))


#end


#admin page

@app.route('/Admin')
def  admindashboard():
    if "admin" in session:
        user = session["admin"]
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail
        return render_template('admin/dashboard.html',user=user,admin=admin,email=email)
    else:
        
        return redirect(url_for('relogin'))
       
    


@app.route('/Admin/user')
def user():
    if "admin" in session:
        user = session["admin"]
        ordinary = (db.session.query(Ordinary).filter(Ordinary.usr_name == Other.usr_name).join(Other,Other.admin_approval == 'no')).all()
        authority = (db.session.query(Authority).filter(Authority.usr_name == Other.usr_name).join(Other,Other.admin_approval == 'no')).all()
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail
        return render_template('admin/user.html',ordinary = ordinary,authority = authority,user=user,admin=admin,email=email)
    else:
        return redirect(url_for('relogin'))


@app.route('/Admin/user/verify/<path:username>/<path:value>')
def verify(username,value):
    if "admin" in session:
        user = session["admin"]
        print(username)
        result = value
        print(result)
        adm = Admin.query.filter_by(usr_name = user).first()
        if adm == None:
            admin_id = user
        else:
            admin_id = adm.admin_id
        verify = Other.query.filter_by(usr_name = username).first()
        if result == 'accept':
            verify.admin_approval = 'accept'
            verify.admin_id = admin_id
            db.session.add(verify)

            user1 = User.query.filter_by(username = username).first()
            print(user1)
            email = user1.mail

            msg = Message('Hello'+' '+ username, sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.html = '<h5>Hi,</h5><h3>&nbsp; {}.<br>I am happy to inform you that, your account is verified successfully</h3>'.format(username)
            mail.send(msg)

            db.session.commit()
            flash('Verified successfully and sent mail ')
            return redirect(url_for('user',user=user))

        elif result == 'reject':
            verify.admin_approval = 'reject'
            verify.admin_id = admin_id
            db.session.add(verify)

            user1 = User.query.filter_by(username = username).first()
            print(user1)
            user1.hash = 'rejected'
            email = user1.mail

            msg = Message('Hello'+' '+ username, sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.html = '<h5>Hi,</h5><h3>&nbsp; {}.<br>I am sorry to inform you that, your account is rejected by Admin</h3>'.format(username)
            mail.send(msg)

            db.session.add(user1)
            db.session.commit()
         
            flash('Verified successfully and sent mail')
            return redirect(url_for('user',user=user))
    else:
        return redirect(url_for('relogin'))

     
         
@app.route('/Admin/process')
def  process():
    if "admin" in session:
        user = session["admin"]
        succ = Other.query.filter_by(third_party_pending_order ='yes' ).all()
        fail = Other.query.filter_by(third_party_pending_order ='reject' ).all()
        processed = Other.query.filter_by(no_of_video_request = 2 ).all()
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail
        print(succ)
        print(fail)
        print(processed)
        return render_template('admin/process.html',succ = succ ,fail = fail ,processed = processed ,user=user,admin=admin,email=email)
    else:
        return redirect(url_for('relogin'))



@app.route('/Admin/processing/<path:uname>')
def  processing(uname):

    if "admin" in session:
            descs = np.load('third_image/'+ uname +'.npy',allow_pickle=True)[()]
            video_path = 'third_video/'+ uname + '.mp4'
            print(video_path)
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                flash('Video cannot Open','error')
                print("Video cannot Open")
                return redirect(url_for('process'))
            _, img_bgr = cap.read()
            padding_size = 0
            resized_width = 2000
            video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
            output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            writer = cv2.VideoWriter('static/result/'+uname+'.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)
            m=-1
            i=1
            s=0
            c=1
            th = THreshhold()
            while True:
                        
                ret, img_bgr = cap.read()
                if not ret:
                    break
    
                img_bgr = cv2.resize(img_bgr, video_size)
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                dets = detector(img_bgr, 1)

                for k, d in enumerate(dets):
                    shape = sp(img_rgb, d)
                    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

                    last_found = {'name': 'unknown', 'dist': th, 'color': (0,0,255),'percent': 0}

                    for name, saved_desc in descs.items():
                        dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                        if dist < last_found['dist']:
                            perce = (1-dist)*100
                            last_found = {'name': "Target", 'dist': dist, 'color': (255,255,255), 'percent': perce}
                            if dist< c:
                                c=dist
                            if m == -1:
                                s = i
                                m=0
                                    
                    cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
                    cv2.putText(img_bgr, last_found['name'] + " (" + str(last_found['percent']) + "%)" , org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=last_found['color'], thickness=2)
                i=i+1
                writer.write(img_bgr)
                    
                
            cap.release()
            writer.release()
            maxacc = (1-c)*100
            print(maxacc)
            time = convert(s/24)
            print(convert(s/24)) 

            send = Other.query.filter_by(usr_name = uname).first()
            send.third_party_issue_id = ''
            send.third_party_pending_order = ''
            send.third_party_response = ''
            send.date = ''
            send.start_time = ''
            send.end_time = ''
            send.no_of_video_request = 2
            send.result_time = time
            send.result_percent = str(maxacc)
            db.session.add(send)

            count = Count.query.filter_by(id = 1).first()
            count.Total_request = count.Total_request + 1
            db.session.add(count)

            db.session.commit()
          
            user1 = User.query.filter_by(username = uname).first()
            email = user1.mail

            msg = Message('Hello'+' '+ uname, sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.html = '<h5>Hi,</h5><h3>&nbsp; {}.<br>Your Video is Ready Please login and check</h3> <br> Click on this link to login <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a>'.format(uname)
            mail.send(msg)
            flash('You have successfully processed the video and sent notification to user','procc')
            return redirect(url_for('process'))

   
    else:
        return redirect(url_for('relogin'))

@app.route('/Admin/sendresponse/<path:username>', methods=['GET', 'POST'])
def sendresponse(username):

    if "admin" in session:
        user1 = User.query.filter_by(username = username).first()
        print(user1)
        email = user1.mail

        msg = Message('Hello'+' '+ username, sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
        msg.html = '<h5>Hi,</h5><h3>&nbsp; {}.<br>We are sorry to inform you that ,your request has been declined by ThirdParty </h3>'.format(username)
        mail.send(msg)
        send = Other.query.filter_by(usr_name = username).first()
        send.third_party_issue_id = ''
        send.third_party_pending_order = ''
        send.third_party_response = ''
        send.date = ''
        send.start_time = ''
        send.end_time = ''
        send.no_of_video_request = 2
        db.session.add(send)

        db.session.commit()
        flash('Successfully sent the mail','procc')
        return redirect(url_for('process'))
    else:
      return redirect(url_for('relogin'))



@app.route('/Admin/Processed/result/<path:filename>', methods=['GET', 'POST'])
def download4(filename):
    if "admin" in session:
        return send_from_directory(directory='static/result', filename=filename)
    else:
      return redirect(url_for('relogin'))




@app.route('/third_video/<path:filename>', methods=['GET', 'POST'])
def download3(filename):
    if "admin" in session:
        return send_from_directory(directory='third_video', filename=filename)
    else:
      return redirect(url_for('relogin'))



@app.route('/ID_Proof/<path:filename>', methods=['GET', 'POST'])
def download2(filename):
    if "admin" in session:
        user = session["admin"]
        return send_from_directory(directory='ID_Proof', filename=filename)
    else:
        return redirect(url_for('relogin'))



@app.route('/Admin/third_party', methods=["GET","POST"])
def third():
    if "admin" in session:
        user = session["admin"]
        all = db.session.query(Third.dept.distinct()).all()
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail

     
        if request.method == "POST":
            dept = request.form['firstList']
            new = request.form['secondList']
            name = request.form['thirdList']
            phone = request.form['phone']
            mail1 = request.form['fourthList']
            
            if dept == 'Other':
                dept = new
            exists = User.query.filter_by(mail = mail1).first()

            if not exists:
            
                v1 = randint(0, 1000)
                v2 = randint(0, 1000)
                value = Count.query.filter_by(id = 1).first()
                uname = dept + '_' + str(value.Third_party+1)
                third_party_id = uname
                psw=str(v1)+name+str(v2)
            
                h = hashlib.md5(psw.encode())
                enpassword = h.hexdigest()

                user2 = User(username=uname,password=enpassword,mail=mail1,hash='',type='Third_party')
                register = Third(usr_name = uname, dept=dept, name=name, phone=phone, third_party_id = third_party_id)
                count = Count.query.filter_by(id = 1).first()
                count.Third_party = count.Third_party + 1
                db.session.add(user2)
                db.session.add(register)
                db.session.add(count)
                db.session.commit()
            
                msg = Message('Welcome to Pinpoint Family', sender = 'pinpoint.four.2020@gmail.com', recipients = [mail1])
                msg.html = '<h5>Hi,</h5><h3>You are addded as Third Party at PINPOINT.<br>Please login PINPOINT using following details</h3><h5> Your Username : {} <br> Password : {}<br><br> Happy to connect with u <BR> Thank you<h5>'.format(uname,psw)

                mail.send(msg)


                
                flash('A new Third Party added successfully','success')
                return render_template('admin/add_third.html',all = all, user=user,admin=admin,email=email)
            else:
                flash('Mail ID already Registered','error')


        if all != None:
            return render_template('admin/add_third.html',all = all,user=user,admin=admin,email=email)
        else:
            return render_template('admin/add_third.html',user=user,admin=admin,email=email)
    else:
        return redirect(url_for('relogin'))




@app.route('/Admin/editprofile', methods=["POST"])
def editadmin():
 if "admin" in session:


    if request.method == "POST":

        email3 = request.form['email']
        use = User.query.filter_by(mail = email3).first()
        if use:
            flash("Email ID Already in Use",'error')
            return redirect(url_for('admindashboard'))


        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        print(fname)
        print(lname)
        print(email)
        print(phone)

        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        print(admin)
        admin.fname = fname
        admin.lname = lname
        admin.phone = phone

        user1 = User.query.filter_by(username = session["admin"]).first()
        user1.mail = email

        db.session.add(user1)
        db.session.add(admin)
        db.session.commit()
        flash("You have successfully updated your profile",'success')
    return redirect(url_for('admindashboard'))
 else:

    return redirect(url_for('relogin'))



@app.route('/Admin/updatepassword', methods=["POST"])
def updateadminpass():
    if "admin" in session:

        if request.method == 'POST':
            currentpass = request.form['oldpass']
            newpassword = request.form['newpass']
            confpassword = request.form['confpass']

            if newpassword == confpassword:
                h = hashlib.md5(currentpass.encode())
                enpassword = h.hexdigest()
                user = User.query.filter_by(username = session["admin"],password = enpassword).first()
                if user:
                    h = hashlib.md5(newpassword.encode())
                    enpassword = h.hexdigest()
                    if user.password == enpassword:
                        flash("You have Entered same Password, Try some other",'error')
                    else:
                        user.password = enpassword
                        db.session.add(user)
                        db.session.commit()
                        flash("Successfully Changed Password",'success')
                else:
                    flash("You Entered Wrong Password",'error')

            else:
                flash("New password is not matching",'error')
        
            return redirect(url_for('admindashboard'))
  
    else:
        return redirect(url_for('relogin'))



@app.route('/Admin/editusername', methods=["POST"])
def edituseradmin():

    if "admin" in session:

        if request.method == 'POST':
            currentuser = request.form['olduser']
            newuser = request.form['newuser']
            confuser = request.form['confuser']

            if newuser == confuser:
                if currentuser == session["admin"]:
                    user = User.query.filter_by(username = currentuser).first()
                    if user:
                        if User.query.filter_by(username = newuser).first():
                            flash("New Username Already exist, Try some other",'error')
                            return redirect(url_for('admindashboard'))
                        else:
                            if user.username == newuser:
                                flash("You have Entered same Username, Try some other",'error')
                                return redirect(url_for('admindashboard'))
                            else:
                                if user.type == "Admin":
                                    ad = Admin.query.filter_by(usr_name = currentuser).first()
                                    ad.usr_name = newuser
                                    user.username = newuser
                                    db.session.add(user)
                                    db.session.add(ad)
                                    db.session.commit()
                                    session["admin"] = newuser
                    
                                    flash("Successfully Changed Username",'success')
                                    return redirect(url_for('admindashboard'))
                    else:
                        flash("You Entered Wrong Username",'error')
                        return redirect(url_for('admindashboard'))
                else:
                    flash("You Entered Wrong Username",'error')
                    return redirect(url_for('admindashboard'))

            else:
                flash("New Username is not matching",'error')
                return redirect(url_for('admindashboard'))

    else:
        return redirect(url_for('relogin'))      



@app.route('/Admin/delete', methods=['POST'])
def deleteadmin():

  if "admin" in session:

    if request.method == 'POST':
        password = request.form['password']
        h = hashlib.md5(password.encode())
        enpassword = h.hexdigest()
        user = User.query.filter_by(username = session["admin"],password = enpassword).first()
        if user:
            delete1 = db.session.query(User).filter(User.username == session["admin"]).first()

            if user.type == "Admin":
                delete2 = Admin.query.filter(Admin.usr_name == session["admin"]).first()
                count = Count.query.filter(Count.id == 1).first()
                count.Admin = count.Admin - 1
        
                db.session.add(count)
                db.session.delete(delete1)
                db.session.delete(delete2)
                db.session.commit()

                session.clear()

                
                return redirect(url_for('index'))
        
        else: 
            flash("You have entered Wrong Password",'error')
            return redirect(url_for('admindashboard'))

        return ""
  else:
      return redirect(url_for('relogin'))




@app.route('/Admin/add_admin', methods=["GET","POST"])

def register():
    if "admin" in session and session["admin"] == "SuperAdmin":
        user2 = session["admin"]
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()    
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail   
        if request.method == "POST":
            uname = request.form['uname']
            email = request.form['mail']
            fname = request.form['fname']
            lname = request.form['lname']
            phone = request.form['phone']

            exists = User.query.filter_by(username = uname).first()
            emailid = User.query.filter_by(mail = email).first()


            if not exists and not emailid:
                
                v1 = randint(0, 1000)
                v2 = randint(100, 999)
                psw=str(v1)+uname+str(v2)
                value = Count.query.filter_by(id = 1).first()
                admin_id = "Admin_" + str(value.Admin+1)

                h = hashlib.md5(psw.encode())
                enpassword = h.hexdigest()

                user = User(username=uname,password=enpassword,mail=email,hash='',type='Admin')
                register = Admin(usr_name = uname,fname=fname,lname=lname, phone=phone, admin_id = admin_id)
                count = Count.query.filter_by(id = 1).first()
                count.Admin = count.Admin + 1
                db.session.add(user)
                db.session.add(register)
                db.session.add(count)
                db.session.commit()
                
                
                msg = Message('Welcome to Pinpoint Family', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
                msg.html = '<h5>Hi {}&emsp;{},</h5><h3>You are addded as admin at PINPOINT.<br>Please login PINPOINT using following details</h3><h5> Your Username : {} <br> Password : {}<br><br> Happy to connect with u <BR> Thank you<h5>'.format(fname,lname,uname,psw)

                mail.send(msg)

                
                flash('A new admin added successfullly','success')
                return render_template('admin/add_admin.html',user=user2,admin=admin,email=email)
            else:
                flash('Username or Email already taken,try something else','error')

            
        return render_template('admin/add_admin.html',user=user2,admin=admin,email=email)
    else:
        return redirect(url_for('relogin'))

@app.route('/Admin/remove_user')
def remove():
    if "admin" in session:
        user = session["admin"]
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail   

        admin1 = Admin.query.all()
        normal= Ordinary.query.all()
        third = Third.query.all()
        officials = Authority.query.all()
        rejected = User.query.filter_by(hash = 'rejected').all()
        
        
        return render_template('admin/remove.html',admin=admin, admin1=admin1,normal=normal,third=third, officials=officials,rejected = rejected,user=user,email=email)
    else:
        return redirect(url_for('relogin'))



@app.route('/Admin/threshold')
def Threshold():
    if "admin" in session and session["admin"] == "SuperAdmin":
        user = session["admin"]
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()

        count = Count.query.filter_by(id = 1).first()
        thres = count.Threshhold

        return render_template('admin/threshhold.html',user=user,admin=admin,thres = thres)    
    else:
        return redirect(url_for('relogin')) 


@app.route('/Admin/Threshold/Update', methods = ['POST'])
def thresupdate():

    if "admin" in session and session["admin"] == "SuperAdmin":
        if request.method == "POST":
            value = request.form['thresvalue']
            count = Count.query.filter_by(id = 1).first()
            count.Threshhold = value
            db.session.add(count)
            db.session.commit()
            flash('Successfullly changed Threshold value','success')
            return redirect(url_for('admindashboard'))   

    else:
        return redirect(url_for('relogin')) 




@app.route('/delete/<string:usr_name>/', methods = ['GET', 'POST'])
def delete2(usr_name):
    if "admin" in session:
        userh = session["admin"]
        user= User.query.filter(User.username == usr_name).first()
        print(usr_name)
        print(user.type)
        count = Count.query.filter_by(id = 1).first()
        


        if user.type == "Admin":
        
            count.Admin = count.Admin - 1
            db.session.add(count)
            mydata = db.session.query(Admin).filter(Admin.usr_name == usr_name).first()
            db.session.delete(mydata)
            db.session.delete(user)

        elif user.type == "Ordinary":
            count.Ordinary = count.Ordinary - 1
            db.session.add(count)
            my_data2=Ordinary.query.filter(usr_name==usr_name).first()
            db.session.delete(my_data2)
            other= Other.query.filter(usr_name == usr_name).first()
            db.session.delete(user)
            db.session.delete(other)


        elif user.type == "Third_party":
            count.Third_party = count.Third_party - 1
            db.session.add(count)
            my_data3=Third.query.filter(usr_name==usr_name).first()
            db.session.delete(my_data3)
            db.session.delete(user)

        elif user.type == "Authority":
            count.Authority = count.Authority - 1
            db.session.add(count)
            my_data4 = Authority.query.filter(usr_name==usr_name).first()
            db.session.delete(my_data4)
            other= Other.query.filter(usr_name == usr_name).first()
            db.session.delete(user)
            db.session.delete(other)



        db.session.commit()
        flash("User Deleted Successfully",'success')
        return redirect(url_for('remove',user=userh))
    else:
        return redirect(url_for('relogin'))




@app.route('/Admin/cleanup')
def  Cleanup():
    if "admin" in session and session["admin"] == "SuperAdmin":
        user = session["admin"]
        admin = Admin.query.filter_by(usr_name = session["admin"]).first()
        user1 = User.query.filter_by(username = session["admin"]).first()
        email = user1.mail
        return render_template('admin/cleanup.html',user=user,admin=admin,email=email)

    else:
        flash("Invalid Access",'error')
        return redirect(url_for('relogin'))


@app.route('/Admin/cleandirectory/<string:foldername>')
def  CleanDir(foldername):
    if "admin" in session and session["admin"] == "SuperAdmin":

        filelist = [f for f in os.listdir(foldername +'/')]
        if filelist != []:
            for f in filelist:
                os.remove(os.path.join(foldername +'/', f))
            flash("Completely Removed All the files in the "+ foldername +" folder",'success')
            return redirect(url_for('Cleanup'))
        else:
            flash(foldername +" folder is empty",'error')
            return redirect(url_for('Cleanup'))

    
    else:
        return redirect(url_for('relogin'))
        
#end


@app.route('/forgot',methods=["POST","GET"])
def forgot():
    if request.method=="POST":
        email = request.form['mail']
        user = request.form['username']

        check = User.query.filter_by(username=user).first()
        if check.hash == "rejected":
            flash('You are Rejected by the Admin','error')
            return redirect(url_for('forgot'))
        if not check:
            flash('Invalid credential,username not found','error')
            return redirect(url_for('forgot'))

        if (check):
            def get_random_string(length=24,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
                return ''.join(random.choice(allowed_chars) for i in range(length))
            hash = get_random_string()
            check.hash = hash
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'pinpoint.four.2020@gmail.com', recipients = [email])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hash
            posta.send(msg)
            flash('Please check your email for password reset link','success')
            return redirect(url_for('forgot'))
        else:
            flash('Invalid credential','error')
            return redirect(url_for('forgot'))
    
    else:
            return render_template('base/forgot.html')
    
    
    
@app.route('/<string:hash>',methods=["GET","POST"])
def hashcode(hash):


    check = User.query.filter(User.hash == hash).first() 
    

    
   
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hash= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('password and confirm password not matched','error')
                return render_template('base/reset.html')
        else:
             return render_template('base/reset.html')
    else:
        return redirect(url_for('index'))




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

#end

if(__name__ == "__main__"):
    app.run(debug=True)




#insert into Count(id,Ordinary,Authority,Admin,Third_party,Total_Real,Total_upload,Total_request,Total_crowd,Threshhold) values (1,0,0,0,0,0,0,0,0,0);
#update Count set Threshhold = 0.43  where id = 1;
#insert into User(username,password,hash,mail,type)values('SuperAdmin','12478e7ad0e39aa9c35be4b9a694ba9b','','pinpoint.four.2020@gmail.com','Admin');


