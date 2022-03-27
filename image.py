
from flask import Flask,flash,redirect,url_for,request,Response,render_template_string
import cv2
import face_recognition
from flask_mysqldb import MySQL
import sys
from PIL import Image

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'company'

mysql = MySQL(app)


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        # Read the frame
        _, img = cap.read()
        # Display
        cv2.imwrite('t.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    # Release the VideoCapture object
    cap.release()

@app.route('/')
def index():
    return render_template_string("""<!DOCTYPE html>
<html>
<head>
<title>Welcome Page</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
      @import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}
.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}
.box{
  height: 300px;
  width: 500px;
  background: #069A8E;
  position:absolute;
  top:170px;
  left:0;
  right:0;
  margin:auto;
  border-radius:20px;
}
.boxfather{
  width:100%;
  position:absolute;
}
.box h1{
  color: white;
  font-size: 5em;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}
.box button{
  position:relative;
  top:120px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
.regButtons{
    display:flex;
    justify-content:center;
    margin:0 auto;
}
.regButtons form{
    display:flex;
    align-items:center;
    justify-content:center;
}
</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
      <div class="box">
        <h1>WELCOME</h1>
        <div class="regButtons">
        <form action="http://127.0.0.1:5000/signup">
          <button name="submit" >Sign Up</button>
        </form>&nbsp&nbsp
        <form action="http://127.0.0.1:5000/login">
          <button  name="submit">Login</button>
        </form>
        </div>
      </div>
    </div>
  </div>
</body>
</html>""")
@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'hello %s please login' % guest
@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest=name))
@app.route('/image')

def image():
    # define a video capture object
    vid = cv2.VideoCapture(0)

    while True:

        # Capture the video frame
        # by frame
        # returns two values
        # flag and the frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the quitting button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Saving the image
            cv2.imwrite("vivek.jpg", frame)
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    return "Image detected successfully"


@app.route('/capture')
def capture():
    """Video streaming"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
<title>Capturing Image For Sign-Up</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
      @import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}
.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}
.boxfather{
  width:100%;
  position:absolute;
  }
.box h1{
  color: white;
  font-size: 5em;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}
button{
  left:40%;
  position:relative;
  top:120px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
button.m{
  left:45%;
  position:relative;
  top:120px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
img.m{
  left:28%;
  position:relative;
  top:70px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
}
</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
    <div class='box'>
    <form>
        <img class='m' id="img" src="{{ url_for('video_feed') }}" class="center">
    </form>
    <form>
         <!-- <button name="submit" formaction="http://127.0.0.1:5000/capture" >Re-Capture</button>
          <button  name="submit" formaction="http://127.0.0.1:5000/capture" >Capture</button><br><br>-->
          <button class='m' formaction='http://127.0.0.1:5000/login' name="submit">Submit</button>
        </form>
        </div>
    </div>
  </div>
</body>
</html>''')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


def gen1():
    cap = cv2.VideoCapture(0)
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        """gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 1)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (170, 255, 0), 1)"""
        # Display
        cv2.imwrite('vivek.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('vivek.jpg', 'rb').read() + b'\r\n')
    # Release the VideoCapture object
    cap.release()

@app.route('/capture1')
def capture1():
    """Video streaming"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
<title>Capturing Image For Login</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
      @import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}
.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}
.boxfather{
  width:100%;
  position:absolute;
  }
.box h1{
  color: white;
  font-size: 5em;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}
button{
  left:40%;
  position:relative;
  top:120px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
button.m{
  left:45%;
  position:relative;
  top:120px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
img.m{
  left:28%;
  position:relative;
  top:70px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
}
</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
    <div class='box'>
    <form>
        <img class='m' id="img" src="{{ url_for('video_feed1') }}" class="center">
    </form>
    <form>
         <!-- <button name="submit" formaction="http://127.0.0.1:5000/capture1" >Re-Capture</button>
          <button  name="submit" formaction="http://127.0.0.1:5000/capture1" >Capture</button><br><br>-->
          <button class='m' formaction='http://127.0.0.1:5000/checkimage' name="submit">Submit</button>
        </form>
        </div>
    </div>
  </div>
</body>
</html>''')

@app.route('/video_feed1')
def video_feed1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen1(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/welcome',methods=['POST','GET'])
def welcome():
    if request.method=='POST':
        user=request.form['nm']
        return redirect(url_for('hello_user',name=user))
    else:
        user=request.args.get('nm')
        return redirect(url_for('hello_user',name=user))

@app.route('/login')
def login():
    try:
        signupimg = face_recognition.load_image_file("t.jpg")
        signupimg = cv2.cvtColor(signupimg, cv2.COLOR_BGR2RGB)
        myface = face_recognition.face_locations(signupimg)[0]
        cv2.rectangle(signupimg, (myface[3], myface[0]), (myface[1], myface[2]), (255, 0, 255), 2)
    except IndexError as e:
        return capture()
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("update customers set img = %s where id = %s ",('t.jpg',id))
        mysql.connection.commit()
        cursor.close()
        return render_template_string("""<!DOCTYPE html>
    <html>
    <head>
    <title>Login Page</title>
    <style>
          @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
    @import url(https://fonts.googleapis.com/css?family=Montserrat:700);

    *{
      margin: 0;
      padding: 0;
    }
    .intro{
      margin: auto;
    }
    .black {
      width: 50%;
      float: left;
      background: #283644;
      height: 100vh;
    }

    .white{
      width: 50%;
      float: right;
      background: #4D727E;
      height: 100vh;
    }

    .box{
      height: 310px;
      width: 500px;
      background: #069A8E;
      position:absolute;
      top:160px;
      left:0;
      right:0;
      margin:auto;
      border-radius:20px;
    }

    .boxfather{
      width:100%;
      position:absolute;
    }
    .box h1{
      color: white;
      font-size: 5em;
      text-align: center;
      position: relative;
      top:40px;
      font-family: 'Montserrat', sans-serif;
    }
    ::placeholder { 
  color: black;
}
    .box p{
      color: white;
      font-size: 19px;
      text-align: center;
      position: relative;
      top:70px;
      font-family: 'Montserrat', sans-serif;
    }

    .box button{
      left:31%;
      position:relative;
      top:80px;
      padding: 8px 20px;
      cursor:pointer;
      border:0;
      outline:none;
      color:black;
      background:white;
      transition:all .3s ease;
      font-size: 19px;
      font-family: montserrat;
      border-radius:5px;
    }
    button.a{
      left:39%;
      position:relative;
      top:80px;
      padding: 8px 20px;
      color:black;
      background:transparent;
      font-size: 9px;
      font-family: montserrat;
    }
    input[type="submit"]{
      border: 0;
      padding: 10px;
      font-family: montserrat;
      text-transform: capitalize;
      color:white;
      border-radius: 10px;
      background-color: black;
    }
    input[type="text"]{
      margin: 10px;
      border: 0;
      padding: 10px;
      font-family: montserrat;
      text-transform: capitalize;
      border-radius: 10px;
    }

    </style>
    </head>
    <body>
      <div class="intro">
        <div class="black"></div>
        <div class="white"></div>
        <div class="boxfather">
          <div class="box">
            <h1>Login</h1>
            <form>
            <p><input type="text" placeholder="User Id : "  /></p>
              <button type="submit" formaction="http://127.0.0.1:5000/capture1">Capture Image</button><br><br>
              <button class='a' formaction="http://127.0.0.1:5000/">by password</button>
            </form>
          </div>
        </div>

      </div>
    </body>
    </html>""")


@app.route('/save', methods=['POST', 'GET'])
def save():
    try:
        if request.method == 'GET':
            return signup()

        if request.method == 'POST':
            global id
            name = request.form['name']
            id = request.form['id']
            password = request.form['password']
            c_password = request.form['c_password']
            cursor = mysql.connection.cursor()
        # cursor.execute("drop table customers")
            cursor.execute("CREATE TABLE if not exists customers (name VARCHAR(255), id VARCHAR(255) primary key,password VARCHAR(255),c_password VARCHAR(255),img LONGBLOB NOT NULL)")
            if name and id and password and c_password:
                if password == c_password:
                    cursor.execute('''INSERT INTO customers (name, id, password, c_password) VALUES (%s, %s, %s, %s)''', (name, id, password, c_password))
                    mysql.connection.commit()
                    cursor.close()
                    return capture()
                else:
                    return signup() and 'password and confirm password should be same'
            else:
                return signup() and 'can not be empty'
    except:
        return signup() and 'user id alreay exists'

@app.route('/signup')
def signup():
    return render_template_string("""<!DOCTYPE html>
<html>
<head>
<title>Sign Up</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
@import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}

.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}

.box{
  height: 470px;
  width: 500px;
  background: #069A8E;
  position:absolute;
  top:120px;
  left:0;
  right:0;
  margin:auto;
  border-radius:20px;
}

.boxfather{
  width:100%;
  position:absolute;
}
.box h1{
  color: white;
  font-size: 5em;
  text-align: center;
  position: relative;
  top:40px;
  font-family: 'Montserrat', sans-serif;
}
::placeholder { 
  color: black;
}
.box p{
  color: black;
  font-size: 19px;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}

.box button{
  left:39%;
  position:relative;
  top:80px;
  padding: 8px 20px;
  cursor:pointer;
  border:0;
  outline:none;
  color:black;
  background:white;
  transition:all .3s ease;
  font-size: 19px;
  font-family: montserrat;
  border-radius:5px;
}
input[type="submit"]{
  border: 0;
  padding: 10px;
  font-family: montserrat;
  text-transform: capitalize;
  border-radius: 10px;
  background-color: black;
}
input[type="text"]{
  margin: 10px;
  border: 0;
  padding: 10px;
  font-family: montserrat;
  text-transform: capitalize;
  border-radius: 10px;
  color: black;
}

</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
      <div class="box">
        <h1>Sign Up</h1>
        <form method='POST'>
        <p><input type="text" name="name" placeholder="Name : "  /></p>
        <p><input type="text" name="id" placeholder="User Id : "  /></p>
          <p><input type="text" name="password" placeholder="Password : "></p>
          <p><input type="text" name="c_password" placeholder="Confirm Password : "></p>
          <!--<button type="submit" formaction="http://127.0.0.1:5000/capture">Capture Image</button><br><br>-->
        <button type="submit" formaction="http://127.0.0.1:5000/save">Submit</button>
        </form>
      </div>
    </div>

  </div>
</body>
</html>""")

@app.route('/success')
def success():
    return render_template_string("""<!DOCTYPE html>
<html>
<head>
<title>Thanks</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
@import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}

.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}

.box{
  height: 500px;
  width: 500px;
  background: #069A8E;
  position:absolute;
  top:150px;
  left:0;
  right:0;
  margin:auto;
  border-radius:20px;
}

.boxfather{
  width:100%;
  position:absolute;
}
.box h1{
  color: #E4E4E4;
  font-size: 3em;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}
.box p{
  color: #E4E4E4;
  font-size: 19px;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}

</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
      <div class="box">
        <h1>Authentication Successful. Thank You</h1>
      </div>
    </div>

  </div>
</body>
</html>""")


@app.route('/fail')
def fail():
    return render_template_string("""<!DOCTYPE html>
<html>
<head>
<title>Thanks</title>
<style>
      @import url(https://fonts.googleapis.com/css?family=Oxygen:400,300);
@import url(https://fonts.googleapis.com/css?family=Montserrat:700);

*{
  margin: 0;
  padding: 0;
}
.intro{
  margin: auto;
}
.black {
  width: 50%;
  float: left;
  background: #283644;
  height: 100vh;
}

.white{
  width: 50%;
  float: right;
  background: #4D727E;
  height: 100vh;
}

.box{
  height: 500px;
  width: 500px;
  background: #069A8E;
  position:absolute;
  top:150px;
  left:0;
  right:0;
  margin:auto;
  border-radius:20px;
}

.boxfather{
  width:100%;
  position:absolute;
}
.box h1{
  color: #E4E4E4;
  font-size: 3em;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}
.box p{
  color: #E4E4E4;
  font-size: 19px;
  text-align: center;
  position: relative;
  top:70px;
  font-family: 'Montserrat', sans-serif;
}

</style>
</head>
<body>
  <div class="intro">
    <div class="black"></div>
    <div class="white"></div>
    <div class="boxfather">
      <div class="box">
        <h1>Authentication Failed. Thank You</h1>
      </div>
    </div>

  </div>
</body>
</html>""")

@app.route('/checkimage')
def checkimage():
    # image = Image.open('t.jpg')
    cursor = mysql.connection.cursor()
    cursor.execute('''select img from customers where id = %S''',id)
    mysql.connection.commit()
    cursor.close()
    baseimg=face_recognition.load_image_file("t.jpg")
    baseimg=cv2.cvtColor(baseimg,cv2.COLOR_BGR2RGB)

    myface=face_recognition.face_locations(baseimg)[0]
    encodemyface=face_recognition.face_encodings(baseimg)[0]
    cv2.rectangle(baseimg,(myface[3],myface[0]),(myface[1],myface[2]),(255,0,255),2)

    sampleimg=face_recognition.load_image_file("vivek.jpg")
    sampleimg=cv2.cvtColor(sampleimg,cv2.COLOR_BGR2RGB)

    try:
        samplefacetest = face_recognition.face_locations(sampleimg)[0]
        encodesamplefacetest = face_recognition.face_encodings(sampleimg)[0]
    except IndexError as e:
        return fail()
        sys.exit()

    cv2.rectangle(sampleimg, (samplefacetest[3], samplefacetest[0]), (samplefacetest[1], samplefacetest[2]), (255, 0, 255), 2)
    result = face_recognition.compare_faces([encodemyface],encodesamplefacetest)

    resultstring = str(result)

    if resultstring == "[True]":
        return success()
    else:
        return fail()

@app.route('/p_cp')
def p_cp():
    render_template_string("""""")

if __name__ == '__main__':
    app.run(debug=True)
