from extensions import *
from models import *
from forms import BouquetForm, FlowerForm, CreateUserForm

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/wh')
def wh():
    return render_template('admin/warehouse/wh_index.html', title="Склад")

@admin.route('/item', methods=['GET', 'POST'])
def wh_item():
    action = request.args.get('action', 'create')
    item_type = request.args.get('item_type', 'bouquet')
    item_id = request.args.get('item_id', None)

    bouquet_form = BouquetForm()
    flower_form = FlowerForm()

    if item_type == 'bouquet':
        form = bouquet_form
        if action == 'edit' and item_id:
            item = Bouquet.query.get(item_id)
            if item:
                form = BouquetForm(obj=item)
    elif item_type == 'flower':
        form = flower_form
        if action == 'edit' and item_id:
            item = Flower.query.get(item_id)
            if item:
                form = FlowerForm(obj=item)

    if form.validate_on_submit():
        if action == 'create':
            if item_type == 'bouquet':
                new_item = Bouquet()
            elif item_type == 'flower':
                new_item = Flower()
        elif action == 'edit' and item_id:
            if item_type == 'bouquet':
                new_item = Bouquet.query.get(item_id)
            elif item_type == 'flower':
                new_item = Flower.query.get(item_id)

        if new_item:
            form.populate_obj(new_item)
            db.session.add(new_item)
            db.session.commit()
            flash(f'{item_type.capitalize()} успешно {"создан" if action == "create" else "обновлен"}', 'success')
            return redirect(url_for('admin.products_list' if item_type == 'bouquet' else 'admin.flower_list', list_item_type=item_type))

    # Отображение ошибок для форм
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}', 'error')

    return render_template('admin/warehouse/item_create.html', action=action, item_type=item_type, form=form, bouquetForm=bouquet_form, flowerForm=flower_form)


"""     if item_type == 'bouquet' and bouquet_form.validate_on_submit():
        # Получение данных из формы
        name = bouquet_form.name.data
        sku = bouquet_form.sku.data
        category = bouquet_form.category.data
        active = bouquet_form.active.data
        description = bouquet_form.description.data
        show_on_site = bouquet_form.show_on_site.data

        # Создание нового объекта Bouquet
        new_bouquet = Bouquet(name=name, 
                              sku=sku, 
                              category=category, 
                              active=active, 
                              description=description, 
                              show_on_site=show_on_site, 
                              image=None)
        
        flash('Букет успешно создан', 'success')
        # Добавление объекта в сессию базы данных и сохранение
        db.session.add(new_bouquet)
        db.session.commit()
        # отображение уведомленя об успешном создании букета и при нажатии на кнопку в форме "Ок" перенапрявляет на ту же страницу
        flash('Букет успешно создан', 'create_success') 
        
        
        return redirect(url_for('admin.products_list'))
    
    elif item_type == 'flower' and flower_form.validate_on_submit():
            name = flower_form.name.data
            sku = flower_form.sku.data
            category = flower_form.category.data
            active = flower_form.active.data
            description = flower_form.description.data
            show_on_site = flower_form.show_on_site.data

            new_flower = Flower(
                name=name,
                sku=sku,
                category=category,
                active=active,
                description=description,
                show_on_site=show_on_site,
                #TODO add image here
                image=None, 
                price_40=flower_form.price_40.data,
                quantity_40=flower_form.quantity_40.data,
                add_to_bouquet_40=flower_form.add_to_bouquet_40.data,
                price_50=flower_form.price_50.data,
                quantity_50=flower_form.quantity_50.data,
                add_to_bouquet_50=flower_form.add_to_bouquet_50.data,
                price_60=flower_form.price_60.data,
                quantity_60=flower_form.quantity_60.data,
                add_to_bouquet_60=flower_form.add_to_bouquet_60.data,
                price_70=flower_form.price_70.data,
                quantity_70=flower_form.quantity_70.data,
                add_to_bouquet_70=flower_form.add_to_bouquet_70.data,
                price_80=flower_form.price_80.data,
                quantity_80=flower_form.quantity_80.data,
                add_to_bouquet_80=flower_form.add_to_bouquet_80.data,
                price_90=flower_form.price_90.data,
                quantity_90=flower_form.quantity_90.data,
                add_to_bouquet_90=flower_form.add_to_bouquet_90.data,
                price_100=flower_form.price_100.data,
                quantity_100=flower_form.quantity_100.data,
                add_to_bouquet_100=flower_form.add_to_bouquet_100.data,
                price_110=flower_form.price_110.data,
                quantity_110=flower_form.quantity_110.data,
                add_to_bouquet_110=flower_form.add_to_bouquet_110.data
            )

            try:
                db.session.add(new_flower)
                db.session.commit()
                flash('Цветок успешно создан', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Цветок с таким SKU уже существует', 'error')

            return redirect(url_for('admin.products_list'))

    # Отображение ошибок для форм
    if item_type == 'bouquet':
        for field, errors in bouquet_form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(bouquet_form, field).label.text}": {error}', 'error')
    elif item_type == 'flower':
        for field, errors in flower_form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(flower_form, field).label.text}": {error}', 'error')
                
    return render_template('admin/warehouse/item_create.html', item_type=item_type, bouquetForm=bouquet_form, flowerForm=flower_form) """

@admin.route('/list/product_list')
@login_required
def products_list():
    list_item_type = request.args.get('list_item_type')
    search_query = request.args.get('search', '')  # Получаем значение параметра search из запроса

    if list_item_type == 'bouquet':
        items = Bouquet.query.filter(Bouquet.name.ilike(f'%{search_query}%')).all()
    elif list_item_type == 'flower':
        items = Flower.query.filter(Flower.name.ilike(f'%{search_query}%')).all()
    else:
        return "Неверный тип элемента", 400  # Возвращаем ошибку 400 Bad Request

    return render_template('admin/warehouse/product_list.html', title="Все товары", items=items, list_item_type=list_item_type, search=search_query)


@admin.route('/list/edit_bouquet/<int:id>', methods=['GET'])
def edit_item(id):
    bouquet = Bouquet.query.get_or_404(id)
    form = BouquetForm(obj=bouquet)
    return render_template('admin/warehouse/edit_bouquet.html', form=form, bouquet=bouquet)
""" Открытие букета в попапе """
@admin.route('/list/open_item/<string:item_type>/<int:id>')
def open_item(item_type, id):
    if item_type == 'bouquet':
        item = Bouquet.query.get_or_404(id)
    elif item_type == 'flower':
        item = Flower.query.get_or_404(id)
    else:
        abort(404)

    return render_template('admin/warehouse/open_item.html', item=item, item_type=item_type)
@admin.route('/delete/<string:item_type>/<int:id>')
def delete_item(item_type, id):
    if item_type == 'bouquet':
        item = Bouquet.query.get_or_404(id)
    elif item_type == 'flower':
        item = Flower.query.get_or_404(id)
    else:
        abort(404)  # Возвращаем ошибку 404 Not Found для недопустимых типов товаров

    db.session.delete(item)
    db.session.commit()
    flash('Товар успешно удален', 'success')
    return redirect(url_for('admin.products_list') + f'?list_item_type={item_type}')

@admin.route('/category_list')
def category_list():
    pass
@admin.route('/gift_list')
def gift_list():
    pass
@admin.route('/decoration_list')
def decoration_list():
    pass

@admin.route('/users')

def user_management():
    users = AppUser.query.all()
    return render_template('admin/user_management.html', users=users)

@admin.route('/users/create_user', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role_key = form.roles.data  # 'admin', 'user', 'content_manager', или 'director'

        # Проверка на уникальность имени пользователя
        existing_user = AppUser.query.filter_by(username=username).first()
        if existing_user:
            flash('Имя пользователя уже занято', 'error')
            return redirect(url_for('admin.create_user'))

        # Находим объект Role по ключу
        role = Role.query.filter_by(name=role_key).first()
        if not role:
            flash('Выбранная роль не найдена', 'error')
            return redirect(url_for('admin.create_user'))

        # Создание нового пользователя с выбранной ролью
        new_user = AppUser(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'), role_id=role.id)
        db.session.add(new_user)
        db.session.commit()

        flash('Пользователь успешно создан', 'success')
        return redirect(url_for('admin.user_management'))

    return render_template('admin/create_user.html', form=form)


@admin.route('/users/delete/<int:user_id>', methods=['POST'])

def delete_user(user_id):
    user = AppUser.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Вы не можете удалить свой собственный аккаунт', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь успешно удален', 'success')
    return redirect(url_for('admin.user_management'))