from sqlalchemy import create_engine, text

engine = create_engine('postgresql://warehouse:password@dwhdb:5432/warehouse')
with engine.connect() as connection:
    # Создайте исполняемый объект из строки SQL-запроса
    query = text("SELECT * FROM public.bouquet;")
    
    # Выполните запрос и получите результат
    result = connection.execute(query)
    
    # Выведите результаты
    for row in result:
        print(row)