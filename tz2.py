from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

def get_product_category_pairs(products_df, categories_df, product_category_links_df):
  """
  Возвращает датафрейм с парами "Имя продукта - Имя категории" и 
  имена продуктов без категорий.

  Args:
    products_df: DataFrame с продуктами (должен иметь столбец "product_name").
    categories_df: DataFrame с категориями (должен иметь столбец "category_name").
    product_category_links_df: DataFrame с связями между продуктами и категориями
                              (должен иметь столбцы "product_id" и "category_id").

  Returns:
    DataFrame с двумя столбцами: "product_name" и "category_name".
  """

  # Соединяем датафреймы продуктов и связей, чтобы получить ID продуктов и их категории
  product_categories = products_df.join(product_category_links_df, on="product_id", how="left")

  # Соединяем результат с датафреймом категорий, чтобы получить имена категорий
  product_categories = product_categories.join(categories_df, on="category_id", how="left")

  # Выбираем нужные столбцы и взрываем столбец с категориями
  product_category_pairs = product_categories.select("product_name", explode("category_name").alias("category_name"))

  # Находим продукты без категорий
  products_without_categories = products_df.join(product_category_links_df, on="product_id", how="left").filter("category_id is NULL").select("product_name")

  # Объединяем два результата в один датафрейм
  return product_category_pairs.union(products_without_categories)

# Пример использования:

# Создаем SparkSession
spark = SparkSession.builder.appName("ProductCategories").getOrCreate()

# Создаем примерные датафреймы
products_df = spark.createDataFrame([
    ("Product A", 1),
    ("Product B", 2),
    ("Product C", 3),
], ["product_name", "product_id"])

categories_df = spark.createDataFrame([
    ("Category X", 1),
    ("Category Y", 2),
], ["category_name", "category_id"])

product_category_links_df = spark.createDataFrame([
    (1, 1),
    (2, 2),
], ["product_id", "category_id"])

# Вызываем функцию и выводим результат
result_df = get_product_category_pairs(products_df, categories_df, product_category_links_df)
result_df.show()

# Закрываем SparkSession
spark.stop()