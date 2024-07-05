import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')  
django.setup()

from faker import Faker
from random import choice
from kada_management.models import Client, Telephone, Diagnostic

# Initialiser Django

# Initialiser Faker
fake = Faker()

def create_fake_clients(n):
    clients = []
    for _ in range(n):
        client = Client(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        client.save()
        clients.append(client)
    return clients

def create_fake_telephones(clients, n):
    telephones = []
    for _ in range(n):
        telephone = Telephone(
            client=choice(clients),
            marque=fake.company(),
            modele=fake.word(),
            imei=fake.unique.imei()
        )
        telephone.save()
        telephones.append(telephone)
    return telephones

def create_fake_diagnostics(telephones, n):
    for _ in range(n):
        diagnostic = Diagnostic(
            telephone=choice(telephones),
            micro=fake.boolean(),
            haut_parleur=fake.boolean(),
            systeme_charge=fake.boolean(),
            ecran=fake.boolean(),
            mot_de_passe=fake.password(),
            empreinte=fake.boolean(),
            face_id=fake.boolean(),
            port_sim=fake.boolean(),
            pochette=fake.boolean(),
            reseau=fake.boolean(),
            imei=fake.unique.imei(),
            batterie=fake.boolean(),
            boutons_allumage=fake.boolean(),
            boutons_volume=fake.boolean(),
            conver=fake.boolean(),
            torche=fake.boolean(),
            commentaires=fake.text(max_nb_chars=200)  # Optionnel
        )
        diagnostic.save()

if __name__ == '__main__':
    num_clients = 10
    num_telephones = 30
    num_diagnostics = 50

    clients = create_fake_clients(num_clients)
    telephones = create_fake_telephones(clients, num_telephones)
    create_fake_diagnostics(telephones, num_diagnostics)
