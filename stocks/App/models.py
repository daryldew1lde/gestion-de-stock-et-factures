from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models import F
from qrcode import QRCode, ERROR_CORRECT_L
import qrcode
from django.db.models import Count
import os
from io import BytesIO
from django.core.files import File




from django.core.files.images import ImageFile

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Categorie(models.Model):
    nom = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(verbose_name="description", blank=True)
    
    def get_produit_count(self):
        """
        This method retrieves the number of Produits associated with the current Categorie instance.
        """
        return self.produits.count()
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["nom"]

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, verbose_name="category", related_name="produits", related_query_name="produit")
    nom = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(verbose_name="description")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="unit price")
    stock = models.IntegerField(verbose_name="stock")
    image = models.ImageField(upload_to='images/produits/', verbose_name="image",blank=True)
    qr_code = models.ImageField(upload_to='images/qr_code', verbose_name="QR code", blank=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["nom"]
        indexes = [
            models.Index(fields=["categorie", "nom"]),
        ]

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    def generate_qr_code(self):
        """
        Generates a QR code containing the product's name and category,
        and saves it directly to the `qr_code` field.
        """
         # generate a QR code from some data
        data = f"Produit: {self.nom}\nCategorie: {self.categorie.nom}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        # create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        # save the image to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        # create a django file from the BytesIO object
        file = File(buffer)
        file.name = f'qr_code-{self.nom}.png' 
        # assign the file to the image field
        self.qr_code = file
        

    def save(self, *args, **kwargs):
      
        self.generate_qr_code() 
        super().save(*args, **kwargs) 



class Facture(models.Model):
    date = models.DateField(verbose_name="date")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="total")
    
    def __str__(self):
        return f"Facture{self.id}_{self.date.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ["-date"]
    

    @property
    def total(self):
        return self.lignes_facture.aggregate(total=models.Sum(F("total")))["total"]

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"pk": self.pk})


class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="product", related_name="lignes_facture", related_query_name="ligne_facture")
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, verbose_name="invoice", related_name="lignes_facture", related_query_name="ligne_facture")
    quantite = models.IntegerField(verbose_name="quantity")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="unit price")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="total", default=None)

    class Meta:
        verbose_name = "LigneFacture"
        verbose_name_plural = "LigneFactures"
        unique_together = [("produit", "facture")]
    
    def __str__(self):
        return self.produit.nom
  













