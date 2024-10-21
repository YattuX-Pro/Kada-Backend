import random
import string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_commercial = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class CommonInfo(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Client(CommonInfo):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

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
    DIAGNOSTIC_TYPE_CHOICES = [
        ('initial', 'Initial'),
        ('technicien', 'Technicien'),
        ('final', 'Final'),
    ]
     
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
    flash = models.BooleanField()
    camera = models.BooleanField(blank=True, null=True)
    frp = models.BooleanField()
    by_pass = models.BooleanField()
    iphone_desactive = models.BooleanField()
    flash_reseau = models.BooleanField()
    diagnostic_type = models.CharField(max_length=20, choices=DIAGNOSTIC_TYPE_CHOICES)
    numero_diagnostic = models.CharField(max_length=15, unique=True, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnostic {self.id} - {self.telephone} - {self.diagnostic_type}"
    
    def telephone_name(self):
        return f"{self.telephone.client.prenom}-{self.telephone.marque}-{self.telephone.imei}"
    
    @property
    def owner(self):
        return f"{self.user.nom} {self.user.prenom}"
    
    def save(self, *args, **kwargs):
        if not self.numero_diagnostic:
            self.numero_diagnostic = self.generate_unique_numero_diagnostic()
        super(Diagnostic, self).save(*args, **kwargs)

    def generate_unique_numero_diagnostic(self):
        while True:
            numero_diagnostic = 'DIAG-' + ''.join(random.choices(string.digits, k=10))
            if not Diagnostic.objects.filter(numero_diagnostic=numero_diagnostic).exists():
                break
        return numero_diagnostic.upper()
   

class Reparation(CommonInfo):
    DIAGNOSTIC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('created', 'Created'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('suspended', 'Suspended')
    ]

    telephone = models.ForeignKey(Telephone, on_delete=models.CASCADE)
    commercial = models.ForeignKey(CustomUser, related_name='reparations_as_commercial', on_delete=models.CASCADE)
    technician = models.ForeignKey(CustomUser, related_name='reparations_as_technician', on_delete=models.CASCADE, null=True, blank=True)
    initial_diagnostic = models.ForeignKey(Diagnostic, related_name='initial_diagnostic', on_delete=models.CASCADE)
    technician_diagnostic = models.ForeignKey(Diagnostic, related_name='technician_diagnostic', on_delete=models.CASCADE, null=True, blank=True)
    final_diagnostic = models.ForeignKey(Diagnostic, related_name='final_diagnostic', on_delete=models.CASCADE, null=True, blank=True)
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    commentaires = models.TextField(blank=True, null=True)
    numero_reparation = models.CharField(max_length=15, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=DIAGNOSTIC_STATUS_CHOICES, default='created')

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
        return f"{self.reparation.telephone.client.prenom} {self.reparation.telephone.client.nom}"
    
    @property
    def numero_reparation(self):
        return f"{self.reparation.numero_reparation}"
    
    @property
    def numero_telephone(self):
        return f"{self.reparation.telephone.client.phone}"
    
    
