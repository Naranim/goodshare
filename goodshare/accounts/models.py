from django.db import models, connection
from django.conf import settings
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser )
from goodshare.goods.models import Good
from goodshare.places.models import Place

RATE_CHOICES = [(x, str(x)) for x in range(0, 11)]
GENDER_CHOICES = (
    (u'M', 'male'),
    (u'F', 'female')
)

def dictFetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class AccountManager(BaseUserManager):
    def create_user(self, alias, first_name,
                    last_name, password,
                    email, gender=None, date_of_birth=None):
        user = self.model(alias=alias,
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          date_of_birth=date_of_birth,
                          gender=gender)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, alias, first_name,
                         last_name, password,
                         email, gender=None, date_of_birth=None):
        user = self.create_user(alias,
                                first_name,
                                last_name,
                                password,
                                email,
                                gender,
                                date_of_birth)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    alias = models.CharField(max_length=30, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name = "email address",
        unique=True,
        max_length=255,
        db_index=True,
        blank=False,
        null=False
    )

    date_of_birth = models.DateField(null=True, help_text="Format: YYYY-MM-DD")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    goods = models.ManyToManyField(Good)
    places = models.ManyToManyField(Place)

    USERNAME_FIELD = "alias"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    objects = AccountManager()

    def get_rate(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AVG(rate) as \"rate\" from ((select lender_rate as \"rate\" from accounts_transaction where lender_id=1)" + \
                        "UNION (select taker_rate as \"rate\" from accounts_transaction where taker_id=1)) as \"q3\";")

        results = dictFetchall(cursor)
        return "-" if results[0]['rate'] is None else results[0]['rate']

    def get_comments(self):
        return Comment.objects.filter(user=self.id).order_by('-date')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comment_user")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comment_creator")
    date = models.DateTimeField()
    comment = models.TextField()


class Transaction(models.Model):
    date = models.DateTimeField()
    good = models.ForeignKey(Good)
    lender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction_lender")
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction_taker")
    finished = models.BooleanField(default=False)
    lender_rate = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)
    taker_rate = models.PositiveIntegerField(choices=RATE_CHOICES, null=True)
