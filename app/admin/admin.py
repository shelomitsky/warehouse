from extensions import *
from models import Bouquet

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
class BouquetForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    category = SelectMultipleField('Категория', choices=[('roses', 'Розы'), ('chrysanthemums', 'Хризантемы'), ('irises', 'Ирисы')])
    active = BooleanField('Активность товара')
    image = FileField('Фото товара', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
    show_on_site = BooleanField('Показывать на сайте')

    def validate_name(self, name):
        # Проверка на уникальность названия букета
        existing_bouquet = Bouquet.query.filter_by(name=name.data).first()
        if existing_bouquet:
            raise ValidationError('Такой букет уже есть!')
@admin.route('/')
def index():
    return render_template('admin/index.html')

@admin.route('/wh')
def wh():
    return render_template('admin/warehouse/wh_index.html', title="Склад")

@admin.route('/create', methods=['GET', 'POST'])
def wh_create():
    form = BouquetForm()

    if form.validate_on_submit():
        # Получение данных из формы
        name = form.name.data
        sku = form.sku.data
        category = form.category.data
        active = form.active.data
        description = form.description.data
        show_on_site = form.show_on_site.data

        # Создание нового объекта Bouquet
        new_bouquet = Bouquet(name=name, sku=sku, category=category, active=active, description=description, show_on_site=show_on_site, image=None)
        flash('Букет успешно создан', 'success')
        # Добавление объекта в сессию базы данных и сохранение
        db.session.add(new_bouquet)
        db.session.commit()
        # отображение уведомленя об успешном создании букета и при нажатии на кнопку в форме "Ок" перенапрявляет на ту же страницу
        flash('Букет успешно создан', 'create_success') 
        
        
        return redirect(url_for('admin.wh_create'))

    # Отображение сообщений об ошибках прямо в форме
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}', 'error')

    return render_template('admin/warehouse/item_create.html', title="Товар", form=form)

@admin.route('/products')
def products_list():
    all_bouquets = Bouquet.query.all()
    return render_template ('admin/warehouse/product_list.html', title="Все товары", items=all_bouquets)
@admin.route('/edit_bouquet/<int:id>', methods=['GET'])
def edit_item(id):
    bouquet = Bouquet.query.get_or_404(id)
    form = BouquetForm(obj=bouquet)
    return render_template('admin/warehouse/edit_bouquet.html', form=form, bouquet=bouquet)
@admin.route('/delete/<int:id>')
def delete_bouquet(id):
    bouquet = Bouquet.query.get_or_404(id)
    db.session.delete(bouquet)
    db.session.commit()
    flash('Товар успешно удален', 'success')
    return redirect(url_for('admin.products_list'))