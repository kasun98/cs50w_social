from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    poster_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    like_count = models.IntegerField(default=0)
    likers = models.JSONField(default=list, null=True)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster_id":self.poster_id.id,
            "like_count":self.like_count,
            "likers": self.likers,
            "content": self.content,
            "datetime": self.datetime.strftime("%b %d %Y, %I:%M %p"),
        }
    
    def fn_likers(self, element=None, method=None):
        if method == "append":
            self.likers.append(element)
            self.save()
        elif method == "remove":
            if element in self.likers:
                self.likers.remove(element)
                self.save()
        elif method == "is_following":
            return element in self.likers
        else:
            return len(self.likers)

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile_id = models.ForeignKey("User", on_delete=models.CASCADE)
    net_followings = models.IntegerField(default=0)
    followings = models.JSONField(default=list, null=True)
    net_followers = models.IntegerField(default=0)
    followers = models.JSONField(default=list, null=True)

    def fn_followings(self, element=None, method=None):
        if method == "append":
            self.followings.append(element)
            self.net_followings += 1
            self.save()
        elif method == "remove":
            if element in self.followings:
                self.followings.remove(element)
                self.net_followings -= 1
                self.save()
        elif method == "is_following":
            return element in self.followings
        else:
            return len(self.followings)
        
    def fn_followers(self, element=None, method=None):
        if method == "append":
            self.followers.append(element)
            self.net_followers += 1
            self.save()
        elif method == "remove":
            if element in self.followers:
                self.followers.remove(element)
                self.net_followers -= 1
                self.save()
        else:
            return len(self.followers)

    

