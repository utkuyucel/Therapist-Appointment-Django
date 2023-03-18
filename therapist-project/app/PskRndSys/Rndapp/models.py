from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import datetime 

## Buradaki Model ile otomatik olarak DB'deki tabloları create/alter edebiliyoruz. 
## Ekstra olarak db üzerinde herhangi bir table eklemeye gerek yok.
# Terapist tablosu
class Terapist(models.Model):
  # Main data
  
  # Cinsiyet seçimi için 3 kategori oluşturuyoruz.
  GENDER_CHOICES = {
    ("E", "Erkek"),
    ("K", "Kadın"),
    ("B", "Belirtilmedi"),
  }
  
  # login olan user ile OneToOne bir ilişki kuruluyor. 
  name = models.TextField(max_length=64)
  second_name = models.TextField(max_length=64)
  phone = PhoneNumberField()
  email = models.EmailField()
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default = "B")
  
  # Methods __str__ -> str / {{trp}} şeklinde çağırıldı zaman bastırılacak olan şey
  def __str__(self) -> str:
    return self.name + " " + self.second_name 
  
  # Tam ismini döndüren fonksiyon. {{trp.get_full_name() şeklinde çağrılır.}}
  def get_full_name(self):
    """
    First name + second name
    """
    full_name = self.name + " " + self.second_name
    return full_name

# Danisan tablosu
class Danisan(models.Model):
  
   # Cinsiyet seçimi için 3 kategori oluşturuyoruz.
  GENDER_CHOICES = {
    ("E", "Erkek"),
    ("K", "Kadın"),
    ("B", "Belirtilmedi"),
  }
  
  # Main data
  name = models.TextField(max_length=64)
  second_name = models.TextField(max_length=64)
  phone = PhoneNumberField()
  email = models.EmailField()
  born = models.DateField()
  price = models.IntegerField()
  gender = models.CharField(max_length=1, default = "B", choices=GENDER_CHOICES)
  
  # FK = PK
  pskId = models.ForeignKey(Terapist, on_delete=models.CASCADE)
  
  # Methods
  # Methods __str__ -> str / {{dns (temsili)}} şeklinde çağırıldı zaman bastırılacak olan şey
  def __str__(self) -> str: 
      return self.name + " " + self.second_name 
  
  # Tam ismini döndüren fonksiyon. {{dns.get_full_name() şeklinde çağrılır.}}
  def get_full_name(self):
    """
    First name + second name
    """
    full_name = self.name + " " + self.second_name
    return full_name


  
class Randevular(models.Model):
  # Relations / OneToMany ilişkiler
  dnsId = models.ForeignKey(Danisan, on_delete=models.CASCADE)
  
  # Main
  rndTime = models.DateTimeField(default=timezone.now().strftime("%d/%m/%Y %H:%M")) ##-> () ekleyebilirsin belki now'a
  passed = models.IntegerField(default = 0)  #Field integer olma sebebi django filters'ın binaryfield desteklememesi.
  
  
  """_trigger_function_explanation_

  
      Her kayıt eklendiğinde, vtde trigger function tetikleniyor. Böylece randevuların saatinin geçip geçmediği kontrol ediliyor.
  """
  
  ## __init__ Methods
  def __str__(self) -> str:
    return str(self.rndTime)
  
  # def save(self, *args, **kwargs):
  #   # Passed or not check at every Add, Update
  #   today = datetime.datetime.now()
  #   randevu_list = Randevular.objects.filter(passed = 0)
  #   # Buraya bir if atarak for içerisine girmesini engelleyebilirsin.
  #   for i in randevu_list:
  #     if (today > i.rndTime):
  #       print("Today", today)
  #       print("i.rndTime", i.rndTime)
  #       i.passed = 1    
  #       super(Randevular, i).save(*args, **kwargs)
    
    # super(Randevular, self).save(*args, **kwargs)

  
  ## Outer Methods
  def passed_or_not(self) -> str:
    if self.passed == 1:
      return "Randevu Tarihi Geçti"
    
    else:
      return "Randevu Tarihi Geçmedi"
  

  



  