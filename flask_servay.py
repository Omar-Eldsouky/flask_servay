from flask import Flask, redirect, request, render_template, flash
from flask_login import UserMixin
from flask_mail import Mail, Message
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b28d23ed689469a408245c16405bb049'

client = MongoClient('mongodb://localhost:27017/')
db = client['DB']
forms = db['forms']



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "omareldsouky14@gmail.com"
app.config['MAIL_PASSWORD'] = "vsqe bqdj lziv coto"
mail = Mail(app)

class form(UserMixin):
    def __init__(self,user_id, customer, email, dealer, rating, comments):
        self.id = user_id
        self.customer = customer
        self.email = email
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


# Existing code...

# Example usage
# send_email('omareldsouky14@example.com', receiver_email=email, subject='Test Subject', body='This is a test email from Flask.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['customer_email']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
    
    if customer=='' or dealer=='' or email=='':
        flash('Please fill out the form', 'danger')
        return redirect('/')
    if forms.find_one({'customer': customer, 'customer_email': email, 'dealer': dealer}):
        flash('You have already submitted a form', 'danger')
        return redirect('/')
    if customer and dealer and rating and comments:
        forms.insert_one({'customer': customer, 'customer_email': email, 'dealer': dealer, 'rating': rating, 'comments': comments})
        msg = Message('New Form Submission', sender='omareldsouky14@gmail.com', recipients=[email])
        msg.body = f'Hello {customer},\n\nThank you for submitting the form. We appreciate your feedback.\n\nDealer: {dealer}\nRating: {rating}\nComments: {comments}\n\nBest Regards,\nOmar Eldsouky'
        mail.send(msg)

        # return 'Thanks for submitting the form'
    else:
        flash('Please fill out the form', 'danger')
        return redirect('/')
        
    return render_template('success.html', title = 'Success')

if __name__ == '__main__':
    app.run(debug=True)