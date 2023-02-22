# /portfolio/views.py
from flask import Blueprint
views = Blueprint('views', __name__)

import base64

from flask import render_template, make_response, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .models import PortfolioItemDB
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length






from .forms import TagForm, PortfolioItemForm
from .models import Tag, Subtag


@views.route('/')
def home():
    response = make_response(render_template('home.html', user=current_user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@views.route('/portfolio')
def portfolio():
    portfolio_items = PortfolioItemDB.get_all_items()

    # Pass the b64encode function to the template as a variable
    template_context = {
        'b64encode': base64.b64encode
    }

    return render_template('portfolio.html', portfolio_items=portfolio_items, **template_context)

@views.route('/github-webhook/', methods=['POST'])
def github_webhook():
    # Verify the authenticity of the webhook request using the secret key
    secret_key = 'phonicssecret'  # Replace with your own secret key
    signature = request.headers.get('X-Hub-Signature')
    if signature != 'sha1=' + hmac.new(secret_key.encode('utf-8'), request.data, hashlib.sha1).hexdigest():
        return 'Invalid signature', 403

    # Pull the latest changes from the GitHub repository
    subprocess.call(['git', 'pull'])

    # Restart the Flask app
    os.kill(os.getpid(), signal.SIGTERM)

    return 'Webhook received', 200

@views.route('/portfolio/new', methods=['GET', 'POST'])
@login_required
def new_portfolio_item():
    if request.method == 'POST':
        title = request.form['title']
        short_desc = request.form['short_desc']
        long_desc = request.form['long_desc']
        image = request.files['image'].read() if 'image' in request.files else None
        demo_link = request.form['demo_link']
        github_link = request.form['github_link']
        tag_ids = request.form.getlist('tags')
        subtag_ids = request.form.getlist('subtags')

        if title and short_desc:
            new_item = PortfolioItemDB(title=title, short_desc=short_desc, long_desc=long_desc, image=image,
                                       demo_link=demo_link, github_link=github_link)
            new_item.save()

            if tag_ids:
                for tag_id in tag_ids:
                    tag = Tag.get_by_id(tag_id)
                    if tag:
                        new_item.tags.append(tag)

            if subtag_ids:
                for subtag_id in subtag_ids:
                    subtag = Subtag.get_by_id(subtag_id)
                    if subtag:
                        new_item.subtags.append(subtag)

            flash('New item has been added!', 'success')
            return redirect(url_for('views.portfolio'))

        flash('Title and Short Description are required!', 'error')

    tags = Tag.get_all()
    subtags = Subtag.get_subtags()
    return render_template('new_portfolio_item.html', tags=tags, subtags=subtags)

@views.route('/portfolio/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_portfolio_item(item_id):
    if request.method == 'POST':
        item = PortfolioItemDB.get_item_by_id(item_id)
        item.delete()
        flash('Portfolio item deleted successfully', 'success')
        return redirect(url_for('views.portfolio'))
    else:
        abort(405)  # Method Not Allowed






@views.route('/create_tag', methods=['GET', 'POST'])
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        name = form.name.data
        tag = Tag.create(name=name)
        return redirect(url_for('views.show_all_tags'))
    return render_template('create_tag.html', form=form)

@views.route('/tags')
def show_all_tags():
    tags = Tag.get_all()
    return render_template('all_tags.html', tags=tags)

@views.route('/edit_tag/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag(tag_id):
    tag = Tag.get_by_id(tag_id)
    form = TagForm(obj=tag)

    if request.method == 'POST':
        form.populate_obj(tag)
        tag.save()
        return redirect(url_for('views.show_all_tags'))
    return render_template('edit_tag.html', tag=tag, form=form)

@views.route('/delete_tag/<int:pk>', methods=['GET', 'POST'])
def delete_tag(pk):
    tag = Tag.get_by_id(pk)
    if tag is None:
        abort(404)
    if request.method == 'POST':
        tag.delete()
        return redirect(url_for('views.show_all_tags'))
    return render_template('delete_tag.html', tag=tag)



@views.route('/edit-portfolio-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_portfolio_item(item_id):
    item = PortfolioItemDB.query.get_or_404(item_id)
    tags = Tag.query.all()
    subtags = Subtag.query.all()
    form = PortfolioItemForm(obj=item)

    if form.validate_on_submit():
        item.title = form.title.data
        item.short_desc = form.short_desc.data
        item.long_desc = form.long_desc.data
        tag_ids = request.form.getlist('tags')
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        item.tags = tags
        subtag_ids = request.form.getlist('subtags')
        subtags = Subtag.query.filter(Subtag.id.in_(subtag_ids)).all()
        item.subtags = subtags

        if form.image.data:  # if a new image has been uploaded
            item.image = form.image.data.read()

        item.save()
        flash('Portfolio item updated successfully!', 'success')
        return redirect(url_for('views.portfolio'))

    # create a set of IDs for the selected tags and subtags
    selected_tags = set(tag.id for tag in item.tags)
    selected_subtags = set(subtag.id for subtag in item.subtags)

    return render_template('edit_portfolio_item.html', item=item, tags=tags, subtags=subtags,
                           selected_tags=selected_tags, selected_subtags=selected_subtags, form=form)



@views.route('/create_subtag', methods=['GET', 'POST'])
@login_required
def create_subtag():
    form = SubtagForm()
    form.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if form.validate_on_submit():
        subtag = Subtag(name=form.name.data, tagid=form.tag.data)
        subtag.create_subtag()
        flash('Subtag created successfully', 'success')
        return redirect(url_for('views.view_all_subtags'))
    return render_template('create_subtag.html', form=form)


class SubtagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    tag = SelectField('Tag', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Subtag')

@views.route('/edit_subtag/<int:subtag_id>', methods=['GET', 'POST'])
@login_required
def edit_subtag(subtag_id):
    subtag = Subtag.query.get(subtag_id)
    form = SubtagForm(obj=subtag)
    if form.validate_on_submit():
        subtag.name = form.name.data
        subtag.description = form.description.data
        db.session.commit()
        flash('Subtag updated successfully', 'success')
        return redirect(url_for('views.view_all_subtags'))
    return render_template('edit_subtag.html', form=form, subtag=subtag)

@views.route('/delete_subtag/<int:subtag_id>', methods=['POST'])
@login_required
def delete_subtag(subtag_id):
    if request.method == 'POST':
        subtag = Subtag.query.get(subtag_id)
        subtag.delete_subtag()
        flash('Subtag deleted successfully', 'success')
        return redirect(url_for('views.view_all_subtags'))
    else:
        abort(405) # Method Not Allowed

@views.route('/view_all_subtags')
@login_required
def view_all_subtags():
    subtags = Subtag.query.all()
    return render_template('view_all_subtags.html', subtags=subtags)