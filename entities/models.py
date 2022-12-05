from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserParent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Origin(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Entity(models.Model):
    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHERS = "Others/Unknown"

    name = models.CharField(max_length=100)
    alternative_name = models.CharField(max_length=100, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=100,
        choices=(
            (GENDER_MALE, GENDER_MALE),
            (GENDER_FEMALE, GENDER_FEMALE),
            (GENDER_OTHERS, GENDER_OTHERS),
        ),
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Hero(Entity):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    headshot = models.ImageField(null=True, blank=True, upload_to="hero_headshots/")
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    is_immortal = models.BooleanField(default=True)

    benevolence_factor = models.PositiveSmallIntegerField(
        help_text="How benevolent this hero is?",
        default=50
    )
    arbitrariness_factor = models.PositiveSmallIntegerField(
        help_text="How arbitrary this hero is?"
    )
    # relationships
    father = models.ForeignKey(
        "self", related_name="children", null=True, blank=True, on_delete=models.SET_NULL
    )
    mother = models.ForeignKey(
        "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    spouse = models.ForeignKey(
        "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name_plural = "Heroes"


# add a model twice to Django admin
class HeroProxy(Hero):

    class Meta:
        proxy = True


class Villain(Entity):
    is_immortal = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=True)

    malevolence_factor = models.PositiveSmallIntegerField(
        help_text="How malevolent this villain is?"
    )
    power_factor = models.PositiveSmallIntegerField(
        help_text="How powerful this villain is?"
    )
    is_unique = models.BooleanField(default=True)
    count = models.PositiveSmallIntegerField(default=1)


class HeroAcquaintance(models.Model):
    "Non family contacts of a Hero"
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.category = self.hero.category
        super().save(*args, **kwargs)

