from django.shortcuts import render
from django.http import HttpResponse

# Data ulasan hardcoded
reviews = [
    {'username': 'user1', 'description': 'Great movie!', 'rating': 5},
    {'username': 'user2', 'description': 'Pretty good.', 'rating': 4},
    {'username': 'user3', 'description': 'Not bad, but could be better.', 'rating': 3},
]

def review_page(request):
    if request.method == 'POST':
        # Menambah ulasan baru
        username = 'user_example'  # Contoh username
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        reviews.insert(0, {'username': username, 'description': description, 'rating': rating})
    
    return render(request, 'ulasan.html', {'reviews': reviews})
