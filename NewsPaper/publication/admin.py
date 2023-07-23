from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_rate(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них
    # это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы
    # выделили галочками.
    queryset.update(rate=0)


nullfy_rate.short_description = 'Обнулить рейтинг'  # описание для более понятного представления в админ панеле
# задаётся, как будто это объект


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Product._meta.get_fields()]  # генерируем список имён всех полей для
    # более красивого отображения
    list_display = ('author', 'choice', 'time_create', 'header', 'rate')  # оставляем только имя и цену товара
    list_filter = ('author', 'time_create', 'category__category_name', 'rate')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'choice', 'time_create', 'category', 'header', 'rate')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rate]  # добавляем действия в список


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
