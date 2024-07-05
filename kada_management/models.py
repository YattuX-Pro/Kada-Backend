from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Telephone(models.Model):
    client = models.ForeignKey(Client,related_name='telephones', on_delete=models.CASCADE)
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    imei = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.client.prenom} {self.marque} - {self.imei}"
    
    @property
    def client_name(self):
        return self.client.prenom

class Diagnostic(models.Model):
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
   

class Panne(models.Model):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Panne {self.id} - {self.telephone}"

class Outil(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Reparation(models.Model):
    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    pannes = models.ManyToManyField(Panne)
    outils_utilises = models.ManyToManyField(Outil)
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reparation {self.id} - {self.telephone}"

class Facture(models.Model):
    reparation = models.OneToOneField(Reparation, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Facture {self.id} - {self.reparation}"
    
    
