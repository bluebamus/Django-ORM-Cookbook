# Django-ORM-Cookbook
Django-ORM-Cookbook

# Site
- [Django ORM Cookbook](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/index.html)
- [Django ORM Cookbook - kor](https://django-orm-cookbook-ko.readthedocs.io/en/latest/index.html)

# Test Environment
- jupyternotebook
  - command : py manage.py shell_plus --notebook
  - settings : settings.py / NOTEBOOK_ARGUMENTS = []

# Note
- 1. [How to find the query associated with a queryset?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query.html)
- You have a model called Event. For getting all records, you will write something like Event.objects.all(), then do str(queryset.query)
    ```
    >>> queryset = Event.objects.all()
    >>> str(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id",
        "events_event"."details", "events_event"."years_ago"
        FROM "events_event"

    >>> queryset = Event.objects.filter(years_ago__gt=5)
    >>> str(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id", "events_event"."details",
    "events_event"."years_ago" FROM "events_event"
    WHERE "events_event"."years_ago" > 5
    ```
- 2. [How to find second largest record using Django ORM ?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/second_largest.html)
  - code :
    ```
    >>> user = User.objects.order_by('-last_login')[1] // Second Highest record w.r.t 'last_login'
    >>> user.first_name
    'Raghu'
    >>> user = User.objects.order_by('-last_login')[2] // Third Highest record w.r.t 'last_login'
    >>> user.first_name
    'Sohan'
    ```
  - sql query :
    ```
    SELECT "auth_user"."id",
            "auth_user"."password",
            "auth_user"."last_login",
            "auth_user"."is_superuser",
            "auth_user"."username",
            "auth_user"."first_name",
            "auth_user"."last_name",
            "auth_user"."email",
            "auth_user"."is_staff",
            "auth_user"."is_active",
            "auth_user"."date_joined"
        FROM "auth_user"
        ORDER BY "auth_user"."last_login" DESC
        LIMIT 1
        OFFSET 2
    ```
- 3. [How to ensure that only one object can be created?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/singleton.html)
  - model to be singleton
    ```
    class Origin(models.Model):
        name = models.CharField(max_length=100)

        def save(self, *args, **kwargs):
            if self.__class__.objects.count():
                self.pk = self.__class__.objects.first().pk
            super().save(*args, **kwargs)
    ```
- 4. 시그널 사용에 대해...
  - ref : [How to update denormalized fields in other models on save](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/update_denormalized_fields.html)
    - 반정규화 필드에 영향을 끼치는 모델을 여러분이 통제할 수 있다면 save 메서드를 재정의합니다.
    - 반정규화 필드에 영향을 끼치는 모델을 여러분이 통제할 수 없다면(그 영향이 라이브러리 등에서 이루어진다면) 시그널을 이용합니다.
- 5. [How to convert string to datetime and store in database?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/datetime.html)
  - code :
    ```
    >>> user = User.objects.get(id=1)
    >>> date_str = "2018-03-11"
    >>> from django.utils.dateparse import parse_date // Way 1
    >>> temp_date = parse_date(date_str)
    >>> a1 = Article(headline="String converted to date", pub_date=temp_date, reporter=user)
    >>> a1.save()
    >>> a1.pub_date
    datetime.date(2018, 3, 11)
    >>> from datetime import datetime // Way 2
    >>> temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    >>> a2 = Article(headline="String converted to date way 2", pub_date=temp_date, reporter=user)
    >>> a2.save()
    >>> a2.pub_date
    datetime.date(2018, 3, 11)
    ```
- 6. [How to convert existing databases to Django models?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/existing_database.html)
    ```
    python manage.py inspectdb

    python manage.py inspectdb > models.py
    ```
- 7. [How to add a model for a database view?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/database_view.html)
    ```
    # create simple view
    create view temp_user as
        select id, first_name from auth_user;

    # related model, by managed = False and db_table="temp_user"
    class TempUser(models.Model):
        first_name = models.CharField(max_length=100)

        class Meta:
            managed = False
            db_table = "temp_user"

    // We can query the newly created view similar to what we do for any table.
    >>> TempUser.objects.all().values()
    <QuerySet [{'first_name': 'Yash', 'id': 1}, {'first_name': 'John', 'id': 2}, {'first_name': 'Ricky', 'id': 3}, {'first_name': 'Sharukh', 'id': 4}, {'first_name': 'Ritesh', 'id': 5}, {'first_name': 'Billy', 'id': 6}, {'first_name': 'Radha', 'id': 7}, {'first_name': 'Raghu', 'id': 9}, {'first_name': 'Rishabh', 'id': 10}, {'first_name': 'John', 'id': 11}, {'first_name': 'Paul', 'id': 12}, {'first_name': 'Johny', 'id': 13}, {'first_name': 'Alien', 'id': 14}]>
    // You cannot insert new reord in a view.
    >>> TempUser.objects.create(first_name='Radhika', id=15)
    Traceback (most recent call last):
    ...
    django.db.utils.OperationalError: cannot modify temp_user because it is a view
    ```
- 8. [What is the difference between null=True and blank=True?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/null_vs_blank.html)
  - 불리언 필드(BooleanField)에 NULL을 입력할 수 있도록 하려면 null=True 를 설정하는 것이 아니라, 널 불리언 필드(NullBooleanField)를 사용해야 합니다.
- 9. [How to use a UUID instead of ID as primary key?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/uuid.html)
    ```
    import uuid
    from django.db import models

    class Event(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        details = models.TextField()
        years_ago = models.PositiveIntegerField()

    >>> eventobject = Event.objects.all()
    >>> eventobject.first().id
    '3cd2b4b0c36f43488a93b3bb72029f46'
    ```
- 10. [How to use slug field with django for more readability?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/slugfield.html)
    ```
    from django.utils.text import slugify
    class Article(models.Model):
        headline = models.CharField(max_length=100)
        . . .
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
            self.slug = slugify(self.headline)
            super(Article, self).save(*args, **kwargs)
        . . .

    >>> u1 = User.objects.get(id=1)
    >>> from datetime import date
    >>> a1 = Article.objects.create(headline="todays market report", pub_date=date(2018, 3, 6), reporter=u1)
    >>> a1.save()
    // slug here is auto-generated, we haven't created it in the above create method.
    >>> a1.slug
    'todays-market-report'
    ```
- 11. [How to add multiple databases to the django application ?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/multiple_databases.html)
  - settings.py : 
    ```
    DATABASE_ROUTERS = ['path.to.DemoRouter']
    DATABASE_APPS_MAPPING = {'user_data': 'users_db',
                            'customer_data':'customers_db'}

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'users_db': {
            'NAME': 'user_data',
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'postgres_user',
            'PASSWORD': 'password'
        },
        'customers_db': {
            'NAME': 'customer_data',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'mysql_cust',
            'PASSWORD': 'root'
        }
    }
    ```
  - Database Router :
    ```
    class DemoRouter:
        """
        A router to control all database operations on models in the
        user application.
        """
        def db_for_read(self, model, **hints):
            """
            Attempts to read user models go to users_db.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def db_for_write(self, model, **hints):
            """
            Attempts to write user models go to users_db.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def allow_relation(self, obj1, obj2, **hints):
            """
            Allow relations if a model in the user app is involved.
            """
            if obj1._meta.app_label == 'user_data' or \
            obj2._meta.app_label == 'user_data':
            return True
            return None

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            """
            Make sure the auth app only appears in the 'users_db'
            database.
            """
            if app_label == 'user_data':
                return db == 'users_db'
            return None
    ```
  - medels.py :
    ```
    class User(models.Model):
        username = models.Charfield(ax_length=100)
        . . .
            class Meta:
            app_label = 'user_data'

    class Customer(models.Model):
        name = models.TextField(max_length=100)
        . . .
            class Meta:
            app_label = 'customer_data'
    ```
  - migrations :
    ```
    python manage.py test --**keepdb**
    ```
- 12. [How to speed tests by reusing database between test runs?](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/keepdb.html)
```
python manage.py test --keepdb
```
- 

# reference
- [Django ORM (QuerySet)구조와 원리 그리고 최적화전략 - 김성렬 - PyCon Korea 2020](https://www.youtube.com/watch?v=EZgLfDrUlrk)
- [[Django] 장고 쿼리셋 파헤치기(Eager Loading)](https://cocook.tistory.com/52)
- [파이콘 한국 2020 / Django ORM 최적화 세션 요약](https://goodlucknua.tistory.com/69)