import calendar
from django.shortcuts import render, redirect
from requests import get
from .models import Danisan, Randevular, Terapist
from .forms import DanisanForm, RandevuForm, TerapistForm
from .filters import RandevuFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now, timedelta
from dateutil.relativedelta import relativedelta
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime


# cache kontrol, çıkış yaptıktan sonra geri butonuna basıldığında, bütün cache'lerin silinmesini sağlıyor.
# login_required, login olmadan bu sayfaya girmemizi engelliyor ve içerisindeki url'e yönlendiriyor.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def anasayfa(request):
  # Datayı çek // Danışanlar, Psikologlar ve randevuların listesi.
  danisan_list = Danisan.objects.all()
  psk_list = Terapist.objects.all()
  rnd_list = Randevular.objects.all()
  
  myFilter = RandevuFilter(request.GET, queryset = rnd_list)
  filtered_rnd = myFilter.qs
  
  # Bugün & Yarın olan randevuları veritabanı üzerinden çekiyoruz.
  day_select_today = Randevular.objects.filter(rndTime__day = now().day, rndTime__month = now().month, rndTime__year = now().year)
  # TODO: Burayı iyice kontrol et. 
  day_select_tom = Randevular.objects.filter(
    rndTime__day = (now().day + timedelta(days=1).days)
    # rndTime__month = (now().month + relativedelta(months=1).days), 
    # rndTime__year = (now().year + relativedelta(months=12).days)
  )
  
  # Templatelerde kullanılacak olan değişkenleri, return ediyoruz.
  return render(request, "home.html", {
    "danisan_list": danisan_list,
    "psk_list":psk_list,
    "rnd_list":rnd_list,
    "time": now,
    "total": danisan_list.count(),
    "number_of_session_today": day_select_today.count(),
    "number_of_session_tomorrow": day_select_tom.count(),
    "day_select_today": day_select_today,
    "day_select_tom": day_select_tom,
    "myFilter":myFilter,
    "filtered_rnd":filtered_rnd,
  })

############################ Danışanlar ############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def danisanlar(request):  
  danisan_list = Danisan.objects.all()
  if request.method == "POST":
    searched = request.POST['searched']
    filtered_danisan_list = Danisan.objects.filter(name__icontains=searched)
    
    return render(request, "danisanlar.html", {
      "danisan_list": danisan_list,
      "total": danisan_list.count(),
      "filtered_danisan_list":filtered_danisan_list
    })
  else:
    return render(request, "danisanlar.html", {
      "danisan_list": danisan_list,
      "total": danisan_list.count()
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def danisanlari_goster(request, danisan_id):
  # danisan = Danisan.objects.get(pk = danisan_id)
  danisan = get_object_or_404(Danisan, pk = danisan_id)
  get_phone = str(danisan.phone)[:3] + "-" + str(danisan.phone)[3:6] + "-" + str(danisan.phone)[6:9] + "-" + str(danisan.phone)[9:]
  
  today_date = date.today()
  danisan_yas = today_date.year - danisan.born.year 
  return render(request, "show_data.html", {
    "danisan": danisan,
    "danisan_yas":danisan_yas,
    "get_phone":get_phone,
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def danisan_ekle(request):
  submitted = False
  
  if request.method == "POST":
    form = DanisanForm(request.POST)  
    if form.is_valid():
      form.save()
      messages.success(request, "Danışan başarıyla eklendi.")
      return HttpResponseRedirect("/danisan_ekle?submitted=True")
  
  else:
    form = DanisanForm
    if "submitted" in request.GET:
      submitted = True
    
  return render(request, "add_danisan.html", {
    "form": form,
    "submitted":submitted
  })
  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def danisan_duzenle(request, danisan_id):
    danisan = get_object_or_404(Danisan, pk = danisan_id)
    form = DanisanForm(request.POST or None, instance = danisan)
    
    if form.is_valid():
      form.save()
      messages.success(request, "Bilgiler başarıyla güncellendi.")
      return redirect("danisanlari-goster", danisan.id)
    
    return render(request, "update_danisan.html", {
      "form": form,
      "danisan": danisan,
  })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def danisan_sil(request, danisan_id):
  # danisan = Danisan.objects.get(pk=danisan_id)
  danisan = get_object_or_404(Danisan, pk=danisan_id)
  danisan.delete()
  messages.success(request, "Danışan başarıyla silindi.")
  return redirect("danisanlar")

  
############################ Randevular ############################  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def randevular(request):  
  randevu_list = Randevular.objects.filter(passed = 0)
  myFilter = RandevuFilter(request.GET, queryset = randevu_list)
  filtered_rnd = myFilter.qs
  
  return render(request, "randevular.html", {
    "randevu_list": randevu_list,
    "filtered_rnd": filtered_rnd,
    "myFilter": myFilter,
    "filtered_total": filtered_rnd.count(),
    "total": randevu_list.count()
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def gecmis_randevular(request):  
  randevu_list = Randevular.objects.filter(passed = 0)
  passed_randevu_list = Randevular.objects.filter(passed = 1)
  myFilter = RandevuFilter(request.GET, queryset = passed_randevu_list)
  filtered_rnd = myFilter.qs
  
  return render(request, "old_randevular.html", {
    "randevu_list": randevu_list,
    "passed_randevu_list": passed_randevu_list,
    "total": passed_randevu_list.count(),
    "myFilter":myFilter,
    "filtered_rnd":filtered_rnd,
    "filtered_total": filtered_rnd.count()
  })
  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def randevulari_goster(request, randevu_id):
  randevu = get_object_or_404(Randevular, pk = randevu_id)
  # danisan = randevu.dnsId.id
  return render(request, "show_randevular.html", {
    "randevu": randevu,
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def randevu_ekle(request):
  submitted = False
  
  if request.method == "POST":
    form = RandevuForm(request.POST)  
    if form.is_valid():
      form.save()
      messages.success(request, "Randevu başarıyla eklendi.")
      return HttpResponseRedirect("/randevu_ekle?submitted=True")
  
  else:
    form = RandevuForm
    if "submitted" in request.GET:
      submitted = True
    
  return render(request, "add_randevu.html", {
    "form": form,
    "submitted":submitted
  })
  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def randevu_duzenle(request, randevu_id):
    randevu = get_object_or_404(Randevular, pk = randevu_id)
    form = RandevuForm(request.POST or None, instance = randevu)
    
    if form.is_valid():
      form.save()
      messages.success(request, "Bilgiler başarıyla güncellendi.")
      return redirect("randevulari-goster", randevu_id)
    
    return render(request, "update_randevu.html", {
      "form": form,
      "randevu": randevu,
  })
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def randevu_sil(request, randevu_id):
  # randevu = Randevular.objects.get(pk=randevu_id)
  randevu = get_object_or_404(Randevular, pk=randevu_id )
  randevu.delete()
  messages.success(request, "Randevu başarıyla silindi.")
  return redirect("randevular")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def tum_randevulari_sil(request):
  randevu = Randevular.objects.all()
  randevu.delete()
  messages.success(request, "Bütün Randevular başarıyla silindi.")
  return redirect("randevular")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapistin_randevulari(request, terapist_id):  
  randevu_list = Randevular.objects.filter(dnsId__pskId = terapist_id, passed = 0)
  terapist = get_object_or_404(Terapist, pk = terapist_id)
  return render(request, "appointment_of_terapist.html", {
    "terapist": terapist,
    "randevu_list": randevu_list,
    "total": randevu_list.count()
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapistin_gecmis_randevulari(request, terapist_id):  
  randevu_list = Randevular.objects.filter(dnsId__pskId = terapist_id, passed = 1)
  terapist = get_object_or_404(Terapist, pk = terapist_id)
  
  return render(request, "passed_appointment_of_terapist.html", {
    "terapist": terapist,
    "randevu_list": randevu_list,
    "total": randevu_list.count()
  })

############################ Terapistler ############################  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapistler(request):  
  terapist_list = Terapist.objects.all()
  
  return render(request, "terapistler.html", {
    "terapist_list":terapist_list,
    "total":terapist_list.count(),
  })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapist_ekle(request):
  submitted = False
  
  if request.method == "POST":
    form = TerapistForm(request.POST)  
    if form.is_valid():
      form.save()
      messages.success(request, "Terapist başarıyla eklendi.")
      return HttpResponseRedirect("/terapist_ekle?submitted=True")
  
  else:
    form = TerapistForm
    if "submitted" in request.GET:
      submitted = True
    
  return render(request, "add_terapist.html", {
    "form": form,
    "submitted":submitted
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapistleri_goster(request, terapist_id):
  terapist = get_object_or_404(Terapist, pk = terapist_id)
  danisanlar = Danisan.objects.filter(pskId = terapist)
  randevular = Randevular.objects.filter(dnsId__in = danisanlar)
  
  get_phone = str(terapist.phone)[:3] + "-" + str(terapist.phone)[3:6] + "-" + str(terapist.phone)[6:9] + "-" + str(terapist.phone)[9:]
  
  return render(request, "show_terapistler.html", {
    "terapist": terapist,
    "danisanlar": danisanlar,
    "danisan_sayisi": danisanlar.count(),
    "randevular": randevular,
    "get_phone": get_phone,
  })
  
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapist_duzenle(request, terapist_id):
    terapist = get_object_or_404(Terapist, pk = terapist_id)
    form = TerapistForm(request.POST or None, instance = terapist)
    
    if form.is_valid():
      form.save()
      messages.success(request, "Bilgiler başarıyla güncellendi.")
      return redirect("terapistleri-goster", terapist_id)
    
    return render(request, "update_terapist.html", {
      "form": form,
      "terapist": terapist,
  })
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def terapist_sil(request, terapist_id):
  # terapist = Terapist.objects.get(pk=terapist_id)  
  terapist = get_object_or_404(Terapist, pk=terapist_id)
  terapist.delete()
  messages.success(request, "Terapist başarıyla silindi.")
  return redirect("terapistler")
  
############################ Diğer ############################  

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url="/login/")
# def takvim(request):  
#   rnd_list = Randevular.objects.all()
#   return render(request, "takvim.html", {
#     "rnd_list": rnd_list
#   })
  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def takvim(request):  
  # pzt = Randevular.objects.filter(rndTime__day)
  """
  pzt içerisinde, pzt olanları filtreleyerek getirecek. bu şekilde tüm takvim yapılabilir.
  """  
  
  gunler = Randevular.objects.filter(passed = 0, rndTime__week = datetime.now().date().isocalendar()[1])

  pzt = gunler.filter(rndTime__iso_week_day = 1)
  sali = gunler.filter(rndTime__iso_week_day = 2)
  cars = gunler.filter(rndTime__iso_week_day = 3)
  pers = gunler.filter(rndTime__iso_week_day = 4)
  cuma = gunler.filter(rndTime__iso_week_day = 5)
  cts = gunler.filter(rndTime__iso_week_day = 6)
  
  return render(request, "takvim.html", {
    "pzt": pzt,
    "sali": sali,
    "cars": cars,
    "pers": pers,
    "cuma": cuma,
    "cts": cts,
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def mesajlar(request):  
  day_select_tom = Randevular.objects.filter(
      rndTime__day = (now().day + timedelta(days=1).days), 
      rndTime__year = (now().year + relativedelta(months=12).days)
    )
    
  day_list = [x.dnsId.email for x in day_select_tom]
  name_list = [x.dnsId for x in day_select_tom]
  randevu_list = [x.rndTime.time() for x in day_select_tom]
  
  if request.method == "POST":
    # message_mail = request.POST['mail-adresi']

    if (len(day_list)) > 0:
      for kisi, rnd, name in zip(day_list, randevu_list, name_list): 
        send_mail(
          "Randevu Bilgilendirmesi - Imago",
          f"Merhabalar Sayın {name}. Yarın Saat {rnd}'de randevunuz bulunmaktadır.\nXXX Psikoterapi Merkezi.",
          settings.DEFAULT_FROM_EMAIL,
          [kisi],
          fail_silently=False,
        )
      
      messages.success(request, "Bilgi Mesajı Başarıyla Gönderildi.")
    
    else:
      messages.info(request, "Randevu Listesi Boş.")
  
  name_list = [x.dnsId.get_full_name() for x in day_select_tom]
  
  return render(request, "mesajlar.html", {
    "day_select_tom": day_list,
    "danisan_list": randevu_list,
    "name_list": name_list,
    "danisan_adet": len(day_list)
  })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def istatistikler(request, danisan_id):  
  
  danisan = get_object_or_404(Danisan, pk = danisan_id)
  # danisan = Danisan.objects.filter(id = danisan_id)
  randevular = Randevular.objects.filter(dnsId = danisan_id, passed = 1)
  
  return render(request, "istatistikler.html", {
    "danisan":danisan,
    "randevu_sayisi": randevular.count(),
    "ucret" : (danisan.price * randevular.count()),
  })

def page_not_found_view(request, exception):
  return render(request, "404.html")