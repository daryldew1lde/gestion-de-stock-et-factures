# In your views.py file

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework import serializers, status
from django.shortcuts import render
from datetime import datetime
from .serializers import *


@api_view(['GET'])
def getProductData(request):
    name = request.GET.get('nom')
    category = request.GET.get('categorie')
    

    if not name or not category:
        return Response({'error': 'Both name and category are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        info = Produit.objects.get(nom=name, categorie__nom=category)
        print(info)
    except Produit.DoesNotExist:
        return Response({'error': 'Produit not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProduitSerializer(info)
    return Response(serializer.data)

@api_view(['GET'])
def createFacture(request):
    date = request.GET.get('date') or datetime.now().strftime('%Y-%m-%d')
    #default total of 0
    total = 0

    data = {'date': date, 'total': total}
    serializer = FactureSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def createLigneFacture(request):
    produit_id = request.GET.get('produit_id')
    facture_id = request.GET.get('facture_id')
    quantite = request.GET.get('quantite', 1)
    prix_unitaire = request.GET.get('prix_unitaire', 0)
    total = int(quantite) * float(prix_unitaire)

    data = {'produit': produit_id, 'facture': facture_id, 'quantite': quantite, 'prix_unitaire': prix_unitaire, 'total': total}
    serializer = LigneFactureSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Your existing views

def produits(request):
    produits = Produit.objects.all()
    return render(request, 'home/produits.html', {'produits':produits, 'segment':'liste2'})

def qr_code(request):
    produits = Produit.objects.all()
    return render(request, 'home/qr_code.html', {'produits':produits, 'segment':'code'})

def details_produit(request):
    id  = request.GET.get('id', None)
    produit = Produit.objects.get(id=id)
    return render(request, 'home/details_produit.html', {'produit':produit})

def modif_produit(request):
    if request.method == 'POST':
        pass
    id  = request.GET.get('id', None)
    produit = Produit.objects.get(id=id)
    return render(request, 'home/modif_produit.html', {'produit':produit})

def index(request):
    if request.GET.get('idcat', None) == None:
        produits = Produit.objects.all()
    else:
        idcat = request.GET.get('idcat')
        categorie = Categorie.objects.get(id=idcat)
        produits = categorie.produits.all()
    return render(request, 'home/index.html', {'produits':produits, 'segment':'Liste'})



def ajouter_produit(request):
    if request.method == 'POST':
        pass
   
    return render(request, 'home/ajouter_produit.html', {'segment':'ajout'})

def home_register(request):
    return render(request, 'home/register.html')


def home_login(request):
    return render(request, 'home/login.html')


def logout(request):
    return render(request, 'home/index.html')


def icons(request):
    return render(request, 'home/icons.html')

def fact(request):
    return render(request, 'home/fact.html', {'segment':'fact'})

def cat(request):
    categories = Categorie.objects.all()
    return render(request, 'home/cat.html', {'segment':'cat', 'categories':categories})


def user(request):
    return render(request, 'home/user.html', {'segment':'user'})













