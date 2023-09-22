from django.contrib import admin
from .models import Member
from .models import Expense
from .models import Split
from .models import Comment
from .models import Notification
from .models import Payment
from .models import Group
from .models import Groupmember

# Register your models here.
admin.site.register(Member)
admin.site.register(Expense)
admin.site.register(Split)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Payment)
admin.site.register(Group)
admin.site.register(Groupmember)