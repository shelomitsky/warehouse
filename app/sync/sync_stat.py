from extensions import *
from models import Option, OptionValueDescription, OptionValue
from flask import Blueprint
import requests
from oc_models import Product, ProductDescription, ProductOption

oc_sync = Blueprint('oc_sync', __name__, template_folder='templates', static_folder='static')

@oc_sync.route('/update_products', methods=['GET', 'POST'])
def update_products():
    message = 'Готовы к обновлению'
    response_status = '200'
    response_data = {}

    if request.method == 'POST':
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')

        if option1:
            # Логика обновления всех товаров
            headers = {
                'X-Oc-Restadmin-Id': 'DtzO0xMlHtNaWykNflsFsSnNMrNBUO3o'
            }

            response = requests.get('http://fm-opencart_engine-1:80/api/rest_admin/products/', headers=headers)
            if response.status_code == 200:
                data = response.json()['data']
                for product_data in data:
                    nullable_fields = [
                        'image',
                        'manufacturer_id',
                        'tax_class_id',
                        'stock_status_id',
                        'weight_class_id',
                        'length_class_id',
                        'rating',
                        'weight',
                        'length',
                        'width',
                        'height',
                        'subtract',
                        'reward',
                        'points',
                        'viewed',
                        'tax_value',
                        'manufacturer'
                    ]
                    nullable_dates = [
                        'date_available',
                        'date_added',
                        'date_modified'
                    ]
                    for field in nullable_dates:
                        if product_data[field] in ('0000-00-00', ''):
                            product_data[field] = None
                    for field in nullable_fields:
                        if product_data[field] == "":
                            product_data[field] = None
                        
                    product = Product(
                        id=product_data['id'],
                        manufacturer=product_data['manufacturer'],
                        sku=product_data['sku'],
                        model=product_data['model'],
                        image=product_data['image'],
                        price=product_data['price'],
                        tax_value=product_data['tax_value'],
                        rating=product_data['rating'],
                        stock_status=product_data['stock_status'],
                        manufacturer_id=product_data['manufacturer_id'],
                        tax_class_id=product_data['tax_class_id'],
                        date_available=product_data['date_available'],
                        weight=product_data['weight'],
                        weight_class_id=product_data['weight_class_id'],
                        length=product_data['length'],
                        width=product_data['width'],
                        height=product_data['height'],
                        length_class_id=product_data['length_class_id'],
                        subtract=product_data['subtract'],
                        sort_order=product_data['sort_order'],
                        status=product_data['status'],
                        stock_status_id=product_data['stock_status_id'],
                        date_added=product_data['date_added'],
                        date_modified=product_data['date_modified'],
                        viewed=product_data['viewed'],
                        reward=product_data['reward'],
                        points=product_data['points'],
                        shipping=product_data['shipping'],
                        quantity=product_data['quantity'],
                        currency_id=product_data['currency_id'],
                        currency_code=product_data['currency_code'],
                        currency_value=product_data['currency_value']
                    )
                    db.session.merge(product)
                    
                    # Adding product descriptions
                    for description_data in product_data['product_description']:
                        description = ProductDescription(
                            product_id=product.id,
                            language_id=description_data['language_id'],
                            name=description_data['name'],
                            description=description_data['description'],
                            meta_description=description_data['meta_description'],
                            meta_keyword=description_data['meta_keyword'],
                            meta_title=description_data['meta_title'],
                            tag=description_data['tag']
                        )
                        db.session.merge(description)
                message = 'Все товары успешно обновлены'
                response_status = response.status_code
                response_data = data
            else:
                message = 'Не удалось обновить товары'
                response_status = response.status_code
                response_data = response.text
        elif option2:
            #TODO Логика для второй опции 
            message = 'На данный момент опция 2 ничего не делает'
        else:
            message = 'Не выбрана ни одна из опций'

    return render_template('admin/sync/debug.html',
                        message=message,
                        response_status=response_status,
                        response_data=response_data)