@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchitemForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''

        '''
        {file:url_for(main.image', filename=file) for file in fs.list()}
        '''
        return redirect(url_for('.index'))

    collection = db.get_collection('users')
    results = collection.find({'user':current_user.id})
    collection = db.get_collection('items')
    collection.update({}, {'$set': {'participation': 'no'}})
    if results != None:
        collection.update_one({'participation_uid': current_user.id}, {'$set': {'participation': 'yes'}})

    return render_template('index.html',
                           item_list=[i for i in db.get_collection('items').find()],
                           file_lst={file: url_for('main.image', filename=file) for file in fs.list()},
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())