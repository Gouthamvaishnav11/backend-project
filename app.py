# from flask import Flask 
from flask import Flask,render_template,request,redirect
# from flask_sqlalchemy import SQalchemy
from flask_sqlalchemy import SQLAlchemy 


# In more detail, Flask(__name__) creates an instance of the Flask class, passing the name of the module (__name__) as an argument. This helps Flask understand where to look for resources such as templates and static files.
# Initialize a new Flask application instance
app=Flask(__name__)

# Connecting flask form sqlite database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///members.db'   

# creating an object of sqlalchemy class
database=SQLAlchemy(app)


# writing python class to insert data into table
class Details(database.Model):
    sno=database.Column(database.Integer,primary_key=True)
    bookName=database.Column(database.String(100),nullable=False)
    Author=database.Column(database.String(100),nullable=False)
    ISBN=database.Column(database.Integer,nullable=False)
   

# first route : index html
# In a Flask application, the @ symbol is used for decorators, which are a way to modify the behavior of functions or methods. The line @app.route('/') is a decorator that Flask provides to map a URL endpoint to a specific function.
# This specific decorator, @app.route('/'), tells Flask that when a user accesses the root URL ('/'), it should call the home function. Decorators in Flask are used to connect URL patterns to view functions, enabling the application to respond to different web requests.
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        # fetch the values of name,author name,isbnumber
        bookname=request.form.get('bookname')
        bookauthor=request.form.get('bookauthor')
        bookisbn=request.form.get('bookisbn')

        # Add it to the database
        Members=Details(bookName=bookname,Author=bookauthor,ISBN=bookisbn)
        database.session.add(Members)
        database.session.commit()

        # returning the index.html
        return redirect('/')
    
    else:
        # fetching all task from the database
        allDetails=Details.query.all()
        # returning the response
        return render_template('index.html',allDetails=allDetails)

# second route : contact html
@app.route('/contact' ,methods=["GET","POST"])
def contact():
    
    # return the respon
    return render_template('contact.html')


# third route :about html
@app.route('/about')
def about():

    # returning the response
    return render_template('about.html')

# fouth route :delete from database
@app.route('/delete')
def delete():
    # extracting the sno
    serial_number=request.args.get('sno')

    # fetching  details with sno=serial_number
    Members=Details.query.filter_by(sno=serial_number).first()

    # deleting the details
    database.session.delete(Members)
    database.session.commit()

    # Reassign serial number
    allDetails=Details.query.order_by(Details.sno).all()
    for index,Members in enumerate(allDetails,start=1):
        Details.sno=index
    database.session.commit()

    # redirect to index.html page
    return redirect('/')

# fifth route:update a task from database
@app.route('/update',methods=["GET","POST"])
def update():
    # Getting the sno for update
    serial_number=request.args.get('sno')

    # fetching the details from database to update details
    reqDetails=Details.query.filter_by(sno=serial_number).first()

    if request.method=="POST":
        # fetching the update values
        updatedbookname=request.form.get('bookname')
        updatedauthorname=request.form.get('bookauthor')
        updatedbookisbn=request.form.get('bookisbn')

        # changing the values of the existing details
        reqDetails.bookName=updatedbookname
        reqDetails.Author=updatedauthorname
        reqDetails.ISBN=updatedbookisbn

        # commting the update in database
        database.session.add(reqDetails)
        database.session.commit()

        # redirecting to index.html
        return redirect('/')
    
    else:
        # rendering the update.html page
        return render_template('update.html',reqDetails=reqDetails)




# app.py runtime
if __name__=='__main__':
    app.run(debug=True,port=4000)



