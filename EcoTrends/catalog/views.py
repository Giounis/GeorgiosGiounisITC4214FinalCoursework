#catalog/views
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category, SubCategory, Comment, Rating
from .forms import CommentForm, ProductFormSet, ProductSearchForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import Http404,HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from accounts.models import SavedProduct
from django.views.decorators.csrf import csrf_protect,csrf_exempt


# Create your views here.

def product_list(request):#returns the product_list template with all the products
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'catalog/product_list.html', context)
def product_search(request): #returns the product_search template with all of the products that match with the query
    search_form = ProductSearchForm(request.GET)
    products = Product.objects.all()

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'search_form': search_form,
    }
    return render(request, 'catalog/product_search.html', context)
def product_list_by_category(request, category_id): #product_list by category
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category=category)
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'catalog/product_list.html', context)

def product_list_by_subcategory(request, subcategory_id):#product_list by subcategory
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    products = Product.objects.filter(subcategory=subcategory)
    categories = Category.objects.all()
    parent_category = subcategory.category
    subcategories = SubCategory.objects.filter(category=parent_category)
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'catalog/product_list.html', context)
class ProductDetailView(LoginRequiredMixin,FormMixin, DetailView):#returns the product detail template
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = '/account/login/'  
    form_class = CommentForm

    def get_context_data(self, **kwargs): #gets data for various fields associated with the respective product
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        context['MEDIA_URL'] = settings.MEDIA_URL

        if self.request.user.is_authenticated:
            context['comments'] = Comment.objects.filter(product=self.object)
            context['saved_products'] = SavedProduct.objects.filter(user=self.request.user, product=self.object)
        else:
            context['comments'] = None
            context['saved_products'] = None

        avg_rating = self.object.average_rating()

        context['avg_rating'] = avg_rating
        return context

    def post(self, request, *args, **kwargs): #the method for the comments
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=401)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.user = request.user
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': reverse('catalog:product_detail', args=[self.get_object().pk])})
            else:
                # If not an AJAX request, redirect back to the same page
                return redirect('catalog:product_detail', pk=self.get_object().pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid form data'}, status=400)
            else:
                context = self.get_context_data()
                context['comment_form'] = form
                return self.render_to_response(context)
@csrf_protect
@require_POST
def save_product(request, product_id): #method for saving products in your profile. What could be called as a "Like" function
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if not SavedProduct.objects.filter(user=user, product=product).exists():
        saved_product = SavedProduct(user=user, product=product)
        saved_product.save()

        return JsonResponse({'success': True, 'message': 'Product saved successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Product is already saved.'})
@login_required
def unsave_product(request, product_id): # the un"like"
    try:
        product_to_unsave = SavedProduct.objects.get(user=request.user, product_id=product_id)
        product_to_unsave.delete()
        message = 'Product unsaved successfully'
        success = True
    except SavedProduct.DoesNotExist:
        message = 'Product not found in saved list'
        success = False
    return JsonResponse({'success': success, 'message': message})

class delete_comment(DeleteView): #comment deletion, which can occur on a comment by the user that made the comment or by an authorized user
    model = Comment

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(self.model, id=comment_id)

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()    
        return JsonResponse({'success': True})

    def get_success_url(self):
        product_id = self.get_object().product.id if self.get_object().product else None

        if product_id:
            return reverse_lazy('catalog:product_detail', kwargs={'pk': product_id})
        else:
            return reverse_lazy('catalog:product_detail')
class delete_commentProfile(DeleteView):#the same method but for deleting comments from the user's profile (they also appear there)
    model = Comment

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(self.model, id=comment_id)

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()    
        return JsonResponse({'success': True})

    def get_success_url(self):
        user_id = self.get_object().user.id if self.get_object().user else None

        if user_id:
            # Constructing the URL manually
            url = f'/account/profile/'
        else:
            # Fallback URL in case user ID is not available
            url = '/account/profile/'

        return url

def rate_index(request: HttpRequest) -> HttpResponse: #method for rating
    products = Product.objects.all()
    for product in products:
        rating = Rating.objects.filter(product=product, user=request.user).first()
        product.user_rating = rating.rating if rating else 0
    return render(request, "index.html", {"products": products})

def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return rate_index(request)
def staff_dashboard_view(request):#view that returns the staff dashboard template
    formset = ProductFormSet(prefix='product')

    if request.method == 'POST':
        formset = ProductFormSet(request.POST, request.FILES, prefix='product')
        if formset.is_valid():
            for form in formset:
                category = form.cleaned_data.get('category')
                subcategory = form.cleaned_data.get('subcategory')

                # Check if the selected subcategory belongs to the chosen category
                if subcategory and subcategory.category != category:
                    # Handle the error, maybe show a message to the user
                    return render(request, 'catalog/error_page.html', {'error_message': 'Invalid category-subcategory relationship'})

                form.save()

            return redirect('product_list')  # Adjust the redirect to match your URL

    return render(request, 'catalog/staff_dashboard.html', {'formset': formset})


@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/login/')
def delete_product(request,product_id):  #method that deletes products. Only authorized users can do that 
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list') 
    return redirect('catalog:product_list')
def get_valid_subcategories(request, category_id):
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})
