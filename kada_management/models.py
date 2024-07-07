import random
import string
from django.db import models
from django.utils import timezone

class CommonInfo(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Client(CommonInfo):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    @property
    def client_fullname(self):
        return f"{self.prenom} {self.nom} : {self.phone}"

class Telephone(CommonInfo):
    client = models.ForeignKey(Client,related_name='telephones', on_delete=models.CASCADE)
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    imei = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.client.prenom} {self.marque} - {self.imei}"
    
    @property
    def client_name(self):
        return f'{self.client.prenom} {self.client.nom} - {self.client.phone}'

class Diagnostic(CommonInfo):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    micro = models.BooleanField()
    haut_parleur = models.BooleanField()
    systeme_charge = models.BooleanField()
    ecran = models.BooleanField()
    empreinte = models.BooleanField()
    face_id = models.BooleanField()
    port_sim = models.BooleanField()
    pochette = models.BooleanField()
    reseau = models.BooleanField()
    batterie = models.BooleanField()
    boutons_allumage = models.BooleanField()
    boutons_volume = models.BooleanField()
    conver = models.BooleanField()
    torche = models.BooleanField()
    is_avant_reparation = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnostic {self.id} - {self.telephone}"
    
    def telephone_name(self):
        return f"{self.telephone.client.prenom}-{self.telephone.marque}-{self.telephone.imei}"
   

class Panne(CommonInfo):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Panne {self.id} - {self.telephone}"

class Outil(CommonInfo):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Reparation(CommonInfo):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    commentaires = models.TextField(blank=True, null=True)
    numero_reparation = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Reparation {self.id} - {self.telephone}"
    
    @property
    def telephone_detail(self):
        return f"{self.telephone.client.prenom}-{self.telephone.marque}-{self.telephone.imei}"
    
    def save(self, *args, **kwargs):
        if not self.numero_reparation:
            self.numero_reparation = self.generate_unique_numero_reparation()
        super(Reparation, self).save(*args, **kwargs)

    def generate_unique_numero_reparation(self):
        while True:
            numero_reparation = 'REP-' + ''.join(random.choices(string.digits, k=10))
            if not Reparation.objects.filter(numero_reparation=numero_reparation).exists():
                break
        return numero_reparation.upper()

class Facture(CommonInfo):
    numero_fature = models.CharField(max_length=15, unique=True, blank=True, null=True)
    reparation = models.OneToOneField(Reparation, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Facture {self.id} - {self.reparation}"
    
    def save(self, *args, **kwargs):
        if not self.numero_fature:
            self.numero_fature = self.generate_unique_numero_facturation()
        super(Facture, self).save(*args, **kwargs)

    def generate_unique_numero_facturation(self):
        while True:
            numero_fature = 'FAC-' + ''.join(random.choices(string.digits, k=10))
            if not Facture.objects.filter(numero_fature=numero_fature).exists():
                break
        return numero_fature.upper()
    
    @property
    def client(self):
        return f"{self.reparation.telephone.client.nom} {self.reparation.telephone.client.prenom}"
    
    @property
    def numero_reparation(self):
        return f"{self.reparation.numero_reparation}"
    
    
