from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Kullanıcı girişi fonksiyonu
def login_user(request):
  # Kullanıcı giriş yaptıysa, anasayfa'ya yönlendir.
  if request.user.is_authenticated:
    return redirect("home")
  
  # Kullanıcı giriş yapmadıysa
  else:
    
    # Login formuna bir veri gönderiyorsa (Login oluyorsa)
    if request.method == "POST":
      
      username = request.POST["username"]
      password = request.POST["password"]
      # kullanıcı adı ve şifre, Django'nun kendi authenticate fonksiyonu içerisinde gönderiliyor 
      user = authenticate(request, username = username, password = password)
      
      # Kullanıcı veritabanında varsa login olup anasayfa'ya yönlendiriliyor
      if user is not None:
        login(request, user)
        return redirect("home")
      
      # Kullanıcı veritabanında yoksa, hata mesajı döndürülüyor ve tekrardan login sayfasına yönlendiriliyor
      else:
        messages.warning(request, ("Kullanıcı adı veya şifre yanlış."))
        return redirect("login")
    
    # Kullanıcı get metodu ile sayfaya geliyorsa, login sayfasını karşısına çıkar.
    else:
      return render(request, "login.html", {})

# Kullanıcı çıkışı fonksiyonu.
# Çıkış yapması için öncelikle giriş yapması gerekli. Bu yüzden login_required decoratorunu kullanıyoruz.
@login_required(login_url="/login/")
def logout_user(request):  
  logout(request)
  messages.success(request, "Başarıyla çıkış yapıldı.")
  return redirect("login")