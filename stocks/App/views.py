# In your views.py file

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.http import JsonResponse
from rest_framework import serializers, status
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout, authenticate
from datetime import datetime
from .serializers import *
from django.db.models import Sum


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
    produit = Produit.objects.get(id=produit_id)
    

    data = {'produit': produit_id, 'facture': facture_id, 'quantite': quantite, 'prix_unitaire': prix_unitaire, 'total': total}
    serializer = LigneFactureSerializer(data=data)

    if serializer.is_valid():
        if produit.stock >= int(quantite):
            produit.stock -= int(quantite)  
            produit.save()
        else:
           return  JsonResponse({'error': 'Stock insufisant', 'restant':produit.stock})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def chart(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    return render(request, 'home/chart.html', {'segment':'chart'})

# Your existing views
def ventes(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    
    # Retrieve the most recent month with records in the database
    last_month = Facture.objects.latest('date').date.month
    data = Facture.objects.filter(date__month=last_month)

    # Annotate the queryset to group by day and sum the montants for each day
    aggregated_data = data.values('date__day').annotate(total_montant=Sum('ligne_facture__total'))

    # Prepare the response lists
    jours = []
    montants = []

    for entry in aggregated_data:
        jours.append(entry['date__day'])
        montants.append(entry['total_montant'])

    # Prepare the response dictionary
    resp = {
        'jours': jours,
        'montants': montants
    }
    
    return JsonResponse(resp, safe=False)
        

def produits(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    produits = Produit.objects.all()
    return render(request, 'home/produits.html', {'produits':produits, 'segment':'liste2'})

def qr_code(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    produits = Produit.objects.all()
    return render(request, 'home/qr_code.html', {'produits':produits, 'segment':'code'})

def details_produit(request):
    if not request.user.is_authenticated:
         return redirect('home_login')

    id  = request.GET.get('id', None)
    produit = Produit.objects.get(id=id)
    return render(request, 'home/details_produit.html', {'produit':produit})

def modif_produit(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    categories = Categorie.objects.all()

    if request.method == 'POST':
    # Extract data from the form
        categorie_nom = request.POST.get('cat')  # Assuming the value of 'cat' is the category ID
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix_unitaire = request.POST.get('prix_unitaire')
        stock = request.POST.get('stock')
        id_produit = request.POST.get('id_produit')
        image = request.FILES.get('image')
        
        
        # Retrieve the category instance
        try:
            categorie = Categorie.objects.get(nom=categorie_nom)
        except:
            categorie = Categorie.objects.create(nom=categorie_nom)
            categorie.save()
        # Create and save the Produit instance
        produit = Produit.objects.get(id=id_produit)
        produit.categorie = categorie
        produit.nom = nom
        produit.description = description
        produit.prix_unitaire = prix_unitaire
        produit.stock = stock
        produit.image = image
        produit.save()
        # Redirect to a success page or product detail page
        return redirect(f'/details_produit?id={produit.id}')  # Assuming there's a URL named 'product_detail'
    id  = request.GET.get('id', None)
    produit = Produit.objects.get(id=id)
    return render(request, 'home/modif_produit.html', {'produit':produit, 'categories':categories})

def index(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    if request.GET.get('idcat', None) == None:
        produits = Produit.objects.all()
    else:
        idcat = request.GET.get('idcat')
        categorie = Categorie.objects.get(id=idcat)
        produits = categorie.produits.all()
    return render(request, 'home/index.html', {'produits':produits, 'segment':'Liste'})



def ajouter_produit(request):
    if not request.user.is_authenticated:
        return redirect('home_login')
    categories = Categorie.objects.all()
    if request.method == 'POST':
        # Extract data from the form
        categorie_nom = request.POST.get('cat')  # Assuming the value of 'cat' is the category ID
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix_unitaire = request.POST.get('prix_unitaire')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        # Retrieve the category instance
        try:
            categorie = Categorie.objects.get(nom=categorie_nom)
        except:
            categorie = Categorie.objects.create(nom=nom)
            categorie.save()
        # Create and save the Produit instance
        produit = Produit.objects.create(
            categorie=categorie,
            nom=nom,
            description=description,
            prix_unitaire=prix_unitaire,
            stock=stock,
            image=image
        )
        produit.save()
        # Redirect to a success page or product detail page
        return redirect(f'/details_produit?id={produit.id}')  # Assuming there's a URL named 'product_detail'

    return render(request, 'home/ajouter_produit.html', {'segment': 'ajout', 'categories': categories})

def suppr_produit(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    id  = request.GET.get('id', None)
    produit = Produit.objects.get(id=id)
    produit.delete()
    return redirect('index')


def suppr_fact(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    id  = request.GET.get('id', None)
    fact = Facture.objects.get(id=id)
    fact.delete()
    return redirect('fact')



def suppruser(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    id  = request.GET.get('id', None)
    us = User.objects.get(id=id)
    us.delete()
    return redirect('user')



def suppr_cat(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    id  = request.GET.get('id', None)
    cat = Categorie.objects.get(id=id)
    cat.delete()
    return redirect('cat')


def home_register(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    return render(request, 'home/register.html')


def home_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'home/login.html', {'error':"nom d'utilisateur ou mot de passe erroné", 'username':username, 'password':password})
        else:
            return render(request, 'home/login.html', {'error':"Veillez replir tout les champs"})
            
    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    return redirect('home_login')


def icons(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    return render(request, 'home/icons.html')


def fact(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    factures = Facture.objects.all()
    return render(request, 'home/fact.html', {'segment':'fact', 'factures':factures})

def details_fact(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    id_fact = request.GET.get('id_fact')
    facture = Facture.objects.get(id=int(id_fact))
    lignesfactures = LigneFacture.objects.filter(facture=facture)
    return render(request, 'home/details_fact.html', {'segment':'fact', 'facture':facture, 'lignesfactures':lignesfactures})

def cat(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    categories = Categorie.objects.all()
    return render(request, 'home/cat.html', {'segment':'cat', 'categories':categories})


def user(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    accounts = User.objects.all()
    return render(request, 'home/user.html', {'segment':'user', 'accounts':accounts})


def createuser(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    if request.method == 'POST':
        nom = request.POST.get('nom')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if not  nom :
            error = 'Vous devez entrer un nom'
        elif pass1 and pass2:
            if pass1!= pass2:
                error = 'Les mots de passe ne correspondent pas'
            else:
                user = User.objects.create_user(username=nom, password=pass1)
                user.save()
                return redirect('user')
    return render(request, 'home/createuser.html')

def modif_user(request):
    if not request.user.is_authenticated:
         return redirect('home_login')
    if request.method == 'POST':
        id = request.POST.get('id')
        nom = request.POST.get('nom')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if not  nom :
            error = 'Vous devez entrer un nom'
        elif pass1 and pass2:
            if pass1!= pass2:
                error = 'Les mots de passe ne correspondent pas'
            else:
                user = User.objects.get(id=id)
                user.username = nom
                user.set_password(pass1)
                user.save()
                return redirect('user')
    id = request.GET.get('id')
    account = User.objects.get(id=id)
    return render(request, 'home/modif_user.html', {'segment':'user', 'account':account})














