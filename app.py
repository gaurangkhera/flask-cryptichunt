from hack import app, create_db,db
from flask import render_template, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from hack.forms import LoginForm, RegForm, HuntForm, QuestionForm, EditUserForm, EditQuesForm
from hack.models import User, Question
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

create_db(app)

@app.route('/')
def home():
    # for i in range(10):
    #     question = Question(ques="hello does your computer have virus", ans='yes')
    #     db.session.add(question)
    #     db.session.commit()
    return render_template('index.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            mess = 'Account already exists'
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            if current_user.is_authenticated and current_user.username != 'xino':
                login_user(new_user, remember=True)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('admin'))
    if current_user.is_authenticated:
        if current_user.username != 'xino':
            return abort(404)
    return render_template('reg.html', form=form, mess=mess)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            mess = 'Email not found'
        else:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                mess = 'Incorrect password'
    if current_user.is_authenticated:
        return abort(404)

    return render_template('login.html', mess=mess, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route('/hunt')
# @login_required
# def hunt():
    # form = HuntForm()
    # ans = form.ans.data
    # maxq = Question.query.order_by(Question.id.desc())
    # if current_user.question > maxq[0].id:
    #     return "You have won the crytpic hutn"
    # if form.validate_on_submit():
    #     if ans.lower == current_user.question.ans:
    #         current_user.correct_ans += 1
    #         current_user.time_taken = datetime.utcnow()
    #         db.session.add(current_user.id)
    #         db.session.commit()
    # return render_template('hunt.html', form=form, user=current_user)

@app.route('/play/<id>', methods=['GET', 'POST'])
@login_required
def play(id):
    mess=''
    question = Question.query.filter_by(id=id).first()
    form = HuntForm()
    maxq = Question.query.all()
    if form.validate_on_submit():
        ans = form.ans.data
        if ans == question.ans:
            mess='correct'
            question = question.id + 1
            current_user.correct_ans += 1
            current_user.ans_time = datetime.now()
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('play', id=question))
        elif ans != question.ans:
            mess='wrong'
    return render_template('hunt.html', question=question, form=form, mess=mess, maxq=maxq)

@app.route('/lb')
def lb():
    users = User.query.order_by(User.correct_ans.desc(), User.ans_time.asc()).all()
    return render_template('leaderboard.html', users=users)

@app.route('/admin')
@login_required
def admin():
    if current_user.username == "xino":
        users = User.query.all()
        questions = Question.query.all()
        return render_template('admin.html', users=users, questions=questions)
    return abort(403)

@app.route('/deleteuser/<id>')
@login_required
def delete_user(id):
    if current_user.username == "xino":
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin'))
    return abort(403)
    
@app.route('/deleteques/<id>')
@login_required
def delete_question(id):
    if current_user.username == "xino":
        question = Question.query.filter_by(id=id).first()
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('admin'))
    return abort(403)

@app.route('/addques', methods=['GET', 'POST'])
@login_required
def add_ques():
    form = QuestionForm()
    if current_user.username == 'xino':
        if form.validate_on_submit():
            question = form.question.data
            answer = form.answer.data
            new_question = Question(ques=question, ans=answer)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('add_question.html', form=form)
    return abort(403)

@app.route('/edituser/<id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.username == 'xino':
        user = User.query.filter_by(id=id).first()
        form = EditUserForm()
        if form.validate_on_submit():
            new_username = form.username.data
            new_email = form.email.data
            new_points = form.points.data
            user.username = new_username
            user.email = new_email
            user.correct_ans = new_points
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('edit_user.html', user=user, form=form)
    return abort(403)

@app.route('/editques/<id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    if current_user.username == 'xino':
        question = Question.query.filter_by(id=id).first()
        form = EditQuesForm()
        if form.validate_on_submit():
            new_ques = form.question.data
            new_ans = form.ans.data
            question.ques = new_ques
            question.ans = new_ans
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('edit_ques.html', form=form, question=question)
    return abort(403)

if __name__ == '__main__':
    app.run(debug=True)

