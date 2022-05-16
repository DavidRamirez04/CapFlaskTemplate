from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import College
from app.classes.forms import CollegeForm, CommentForm
from flask_login import login_required
import datetime as dt

@app.route('/college/new', methods=['GET', 'POST'])
@login_required
def collegeNew():
    form = CollegeForm()
    if form.validate_on_submit():
        newCollege = College(
            school = form.school.data,
            location = form.location.data,
            tuition_in = form.tuition_in.data,
            tuition_out = form.tuition_out.data,
            acceptance = form.acceptance.data,
            grad_rate = form.grad_rate.data,
            ranking = form.ranking.data,
            description = form.description.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        newCollege.save()

        return redirect(url_for('college',collegeID=newCollege.id))

    return render_template('collegeform.html',form=form)

 
@app.route('/college/<collegeID>')
@login_required
def college(collegeID):
    thisCollege = College.objects.get(id=collegeID)
    return render_template('college.html',college=thisCollege)

@app.route('/college/edit/<collegeID>', methods=['GET', 'POST'])
@login_required
def collegeEdit(collegeID):
    editCollege = College.objects.get(id=collegeID)
    if current_user != editCollege.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('college',collegeID=collegeID))
    form = CollegeForm()
    if form.validate_on_submit():
        editCollege.update(
            school = form.school.data,
            location = form.location.data,
            tuition_in = form.tuition_in.data,
            tuition_out = form.tuition_out.data,
            acceptance = form.acceptance.data,
            grad_rate = form.grad_rate.data,
            ranking = form.ranking.data,
            description = form.description.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('college',collegeID=collegeID))

    form.school.data = editCollege.school
    form.location.data = editCollege.school
    form.tuition_in.data = editCollege.tuition_in
    form.tuition_out.data = editCollege.tuition_out
    form.acceptance.data = editCollege.acceptance
    form.grad_rate.data = editCollege.grad_rate
    form.ranking.data = editCollege.ranking
    form.description.data = editCollege.description


    return render_template('collegeform.html',form=form)



@app.route('/college/delete/<collegeID>')
@login_required
def collegeDelete(collegeID):
    deletePost = College.objects.get(id=collegeID)
    if current_user == deletePost.author:
        deletePost.delete()
        flash('The School was deleted.')
    else:
        flash("You can't delete a post you don't own.")
    colleges = College.objects()  
    return render_template('colleges.html',colleges=colleges)

@app.route('/college/list')
def collegeList():
    colleges = College.objects()
    return render_template('colleges.html',colleges = colleges)