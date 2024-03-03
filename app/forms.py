from extensions import *
class BouquetForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    category = SelectMultipleField('Категория', choices=[('roses', 'Розы'), ('chrysanthemums', 'Хризантемы'), ('irises', 'Ирисы')])
    active = BooleanField('Активность товара')
    image = FileField('Фото товара', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
    show_on_site = BooleanField('Показывать на сайте')


class FlowerForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    category = SelectMultipleField('Категория', choices=[('roses', 'Розы'), ('chrysanthemums', 'Хризантемы'), ('irises', 'Ирисы')])
    active = BooleanField('Активность товара')
    image = FileField('Фото товара', validators=[FileAllowed(['jpg', 'png'], 'Только изображения!')])
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
    show_on_site = BooleanField('Показывать на сайте')
    
    price_40 = DecimalField('Цена за 40 см', validators=[Optional()], default=0)
    quantity_40 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_40 = BooleanField('Добавить в букет', default=False)

    price_50 = DecimalField('Цена за 50 см', validators=[Optional()], default=0)
    quantity_50 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_50 = BooleanField('Добавить в букет', default=False)

    price_60 = DecimalField('Цена за 60 см', validators=[Optional()], default=0)
    quantity_60 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_60 = BooleanField('Добавить в букет', default=False)
    
    price_70 = DecimalField('Цена за 70 см', validators=[Optional()], default=0)
    quantity_70 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_70 = BooleanField('Добавить в букет', default=False)
    
    price_80 = DecimalField('Цена за 80 см', validators=[Optional()], default=0)
    quantity_80 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_80 = BooleanField('Добавить в букет', default=False)
    
    price_90 = DecimalField('Цена за 90 см', validators=[Optional()], default=0)
    quantity_90 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_90 = BooleanField('Добавить в букет', default=False)
    
    price_100 = DecimalField('Цена за 100 см', validators=[Optional()], default=0)
    quantity_100 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_100 = BooleanField('Добавить в букет', default=False)
    
    price_110 = DecimalField('Цена за 110 см', validators=[Optional()], default=0)
    quantity_110 = DecimalField('Количество', validators=[Optional()], default=0)
    add_to_bouquet_110 = BooleanField('Добавить в букет', default=False)