from django.urls import path
from . import views

urlpatterns = [
    path("", views.anasayfa, name = "home"),
    path("danisanlar/", views.danisanlar, name = "danisanlar"),
    path("danisan_ekle/", views.danisan_ekle, name="danisan-ekle"),
    path("danisan/<danisan_id>", views.danisanlari_goster, name = "danisanlari-goster"),
    path("danisan_duzenle/<danisan_id>", views.danisan_duzenle, name = "danisan-duzenle"),
    path("danisan_sil/<danisan_id>", views.danisan_sil, name="danisan-sil"),
    path("randevular/", views.randevular, name = "randevular"),
    path("randevular/<terapist_id>", views.terapistin_randevulari, name = "terapistin-randevulari"),
    path("gecmis_randevular/<terapist_id>", views.terapistin_gecmis_randevulari, name = "terapistin-gecmis-randevulari"),
    path("gecmis_randevular/", views.gecmis_randevular, name = "gecmis-randevular"),
    path("randevu_ekle", views.randevu_ekle, name = "randevu-ekle"),
    path("randevu/<randevu_id>", views.randevulari_goster, name = "randevulari-goster"),
    path("randevu_duzenle/<randevu_id>", views.randevu_duzenle, name = "randevu-duzenle"),
    path("randevu_sil/<randevu_id>", views.randevu_sil, name="randevu-sil"),
    path("tum_randevulari_sil/", views.tum_randevulari_sil, name="tum-randevulari-sil"),
    path("terapistler/", views.terapistler, name = "terapistler"),
    path("terapist_ekle", views.terapist_ekle, name = "terapist-ekle"),
    path("terapist/<terapist_id>", views.terapistleri_goster, name = "terapistleri-goster"),
    path("terapist_duzenle/<terapist_id>", views.terapist_duzenle, name = "terapist-duzenle"),
    path("terapist_sil/<terapist_id>", views.terapist_sil, name = "terapist-sil"),
    path("mesajlar/", views.mesajlar, name = "mesajlar"),
    path("istatistikler/<danisan_id>", views.istatistikler, name = "istatistikler"),
    path("takvim/", views.takvim, name = "takvim"),
]

