from django.db import models
from django.contrib.auth.models import User
from django.contrib. auth import get_user_model
from django.db.models import Avg

# Added import statement for the Rating model

class Comment(models.Model):#ensuring that a comment saves all of its attributes
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):#ensuring that the product is associated with all the needed fields. For some reason I never managed to migrate the rating as such, thus I aborted the recommender app (it was a requirement)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='created_products',
        default=get_user_model().objects.get(username='giorgos').pk,
    )
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
        
    def average_rating(self) -> float:
        return Rating.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    @property
    def avg_rating(self):
        return self.average_rating()

    @property
    def rating(self):
        return self.avg_rating

class SavedProduct(models.Model): #model for the "Like"
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'product')
class Rating(models.Model):  #model for the star ratings
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"
