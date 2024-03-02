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
def index(request):
    return render(request, 'index.html')













