# /portfolio/views.py

from flask import Blueprint, render_template, make_response, request
from flask_login import login_required, current_user
from .models import PortfolioItemDB

views = Blueprint('views', __name__)


@views.route('/')
def home():
    response = make_response(render_template('home.html', user=current_user))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@views.route('/portfolio')
def portfolio():
    portfolio_items = PortfolioItemDB.get_all_items()
    return render_template('portfolio.html', portfolio_items=portfolio_items)


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

        if title and short_desc:
            new_item = PortfolioItemDB(title=title, short_desc=short_desc, long_desc=long_desc, image=image,
                                       demo_link=demo_link, github_link=github_link)
            new_item.save()
            flash('New item has been added!', 'success')
            return redirect(url_for('views.portfolio'))

        flash('Title and Short Description are required!', 'error')

    return render_template('new_portfolio_item.html')


@views.route('/portfolio/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio_item(item_id):
    item = PortfolioItemDB.get_item_by_id(item_id)

    if request.method == 'POST':
        item.title = request.form['title']
        item.short_desc = request.form['short_desc']
        item.long_desc = request.form['long_desc']
        item.image = request.files['image'].read() if 'image' in request.files else item.image
        item.demo_link = request.form['demo_link']
        item.github_link = request.form['github_link']

        if item.title and item.short_desc:
            item.save()
            flash('Item has been updated!', 'success')
            return redirect(url_for('views.portfolio'))

        flash('Title and Short Description are required!', 'error')

    return render_template('edit_portfolio_item.html', item=item)


@views.route('/portfolio/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_portfolio_item(item_id):
    item = PortfolioItemDB.get_item_by_id(item_id)
    if item:
        item.delete()
        flash('Item has been deleted!', 'success')
    return redirect(url_for('views.portfolio'))