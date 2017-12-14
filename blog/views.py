from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PIL import Image
from dateutil import parser
# from clarifai.rest import ClarifaiApp


from .models import Post, Tag, Content
from .forms import PostForm
from .getGPS import get_lat_lon_dt

# app = ClarifaiApp()
# model = app.models.get('general-v1.3')
# forbidden = ['backlit', 'light', 'no person', 'silhouette', 'sky']

# Create your views here.
def index(request):
    post_list = Post.objects.filter(is_published=True)
    return render(request, 'blog/index.html', {'post_list': post_list})

def post_detail(request):
    id = request.GET.get('id')
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/partial/post_detail.html', {'post': post})

@login_required
def my_history(request):
    post_list = Post.objects.filter(create_user=request.user)
    return render(request, 'blog/my_history.html', {'post_list':post_list})

@login_required
def current_location_post(request):
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    post_list = Post.objects.filter(is_published=True, lat__range=(lat - 0.3, lat + 0.3), lng__range=(lng - 0.3, lng + 0.3))
    return render(request, 'blog/index.html', {'post_list': post_list})

@login_required
def current_location(request):
    return render(request, 'blog/current_location.html')


@login_required
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_user = request.user
            post.save()

            pictures = request.FILES.getlist('pictures')
            tag_total = set()
        # Multi Files
            for file in pictures:
                content = Content()
            # Read Position from Picture
                content.file = file
                image = Image.open(file)
                lat, lng, dt = get_lat_lon_dt(image)
                if lat:
                    content.lat = lat
                    content.lng = lng
                if dt:
                    dt = parser.parse(dt)
                    content.taken_dt = dt

                content.save()
                post.contents.add(content)

                # response = model.predict_by_filename('.' + content.file.url)
                # concepts = response['outputs'][0]['data']['concepts']
                # tag_array = []
                # for concept in concepts:
                #     if concept['value'] > 0.95:
                #         if concept['name'] not in forbidden:
                #             obj, created = Tag.objects.get_or_create(tag=concept['name'])
                #             tag_array.append(obj)
                # content.tags.set(tag_array)
                # tag_total.update(tag_array)

            # tag_total = list(tag_total)
            # post.tags.set(tag_total)
            post.lat = lat
            post.lng = lng
            post.save()


            return redirect('blog:index')

    else:
        form = PostForm()
        return render(request, 'blog/post_add.html', {'form': form})