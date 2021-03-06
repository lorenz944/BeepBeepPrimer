from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User
from monolith.auth import admin_required
from monolith.forms import UserForm, RemoveUserForm


users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data) #pw should be hashed with some salt
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('create_user.html', form=form)


@users.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
        form = RemoveUserForm()
        if request.method == 'POST':
                if form.validate_on_submit():
                        email, password = form.data['email'], form.data['password']
                        q = db.session.query(User).filter(User.email == email)
                        user = q.first()
                        print(user is None)
                        print(user.authenticate(password))
                        if user is not None and user.authenticate(password):
                                db.session.delete(user)
                                db.session.commit()
                                return redirect('/users')

        return render_template('remove_user.html', form=form)
