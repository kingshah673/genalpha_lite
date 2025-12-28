from django.shortcuts import render

def about(request):
    """About us page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact page"""
    return render(request, 'pages/contact.html')

def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'pages/privacy_policy.html')

def returns_policy(request):
    """Returns policy page"""
    return render(request, 'pages/returns_policy.html')
