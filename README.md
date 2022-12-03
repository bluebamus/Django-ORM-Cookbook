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
- 