from django.db import models

class Users(models.Model):
    uid = models.CharField(primary_key=True, max_length=50)
    username = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)  # ✅ removed unique=True
    lastname = models.CharField(max_length=50, null=True, blank=True)   # ✅ removed unique=True
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'users'

    @property
    def profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return "https://cdn-icons-png.flaticon.com/128/149/149071.png"

    def __str__(self):
        return self.username



class ProfileBio(models.Model):
    profile_uid = models.OneToOneField(
        Users,
        to_field='uid',             # ✅ Explicitly reference Users.uid
        db_column='profile_uid',    # ✅ Exact column name in DB
        on_delete=models.CASCADE,
        related_name='profile_bio'
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'profile_bio'

    def __str__(self):
        return f"{self.profile_uid.username}'s Profile"


from django.db import models

class Arts(models.Model):
    CATEGORY_CHOICES = [
        ('3D Art', '3D Art'),
        ('2D Art', '2D Art'),
        ('Pixel Art', 'Pixel Art'),
        ('Concept Art', 'Concept Art'),
        ('Illustration', 'Illustration'),
        ('Sculptures', 'Sculptures'),
        ('Motion Graphics', 'Motion Graphics'),
        ('Animation', 'Animation'),
        ('Photography', 'Photography'),
        ('Game Assets', 'Game Assets'),
    ]

    art_id = models.CharField(primary_key=True, max_length=50)
    uid = models.ForeignKey(
        'Users',
        to_field='uid',
        db_column='uid',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='2D Art'  # You can change this default
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'arts'

    def __str__(self):
        return f"{self.title} ({self.category})"



class Comments(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=50)
    art = models.ForeignKey(Arts, to_field='art_id', db_column='art_id', on_delete=models.CASCADE)
    uid = models.ForeignKey(Users, to_field='uid', db_column='uid', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'comments'


class Chats(models.Model):
    chat_id = models.CharField(primary_key=True, max_length=50)
    sender_uid = models.ForeignKey(
        Users, to_field='uid', db_column='sender_uid',
        on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver_uid = models.ForeignKey(
        Users, to_field='uid', db_column='receiver_uid',
        on_delete=models.CASCADE, related_name='received_messages'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'chats'


class ArtLikes(models.Model):
    like_id = models.CharField(primary_key=True, max_length=50)
    art = models.ForeignKey(Arts, to_field='art_id', db_column='art_id', on_delete=models.CASCADE)
    uid = models.ForeignKey(Users, to_field='uid', db_column='uid', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'art_likes'
