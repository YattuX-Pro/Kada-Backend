from rest_framework import serializers
from .models import Client, Telephone, Diagnostic, Panne, Outil, Reparation, Facture



class TelephoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telephone
        fields = ['id', 'client', 'marque', 'modele', 'imei', 'client_name']


class ClientSerializer(serializers.ModelSerializer):
    telephones = TelephoneSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'nom', 'prenom', 'email', 'phone', 'telephones', 'client_fullname']


class DiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = [
            'id',
            'telephone',
            'date',
            'micro',
            'haut_parleur',
            'systeme_charge',
            'ecran',
            'empreinte',
            'face_id',
            'port_sim',
            'pochette',
            'reseau',
            'batterie',
            'boutons_allumage',
            'boutons_volume',
            'conver',
            'torche',
            'is_avant_reparation',
            'telephone_name'
        ]
        read_only_fields = ['id', 'date']

class PanneSerializer(serializers.ModelSerializer):
    telephone = TelephoneSerializer(read_only=True)

    class Meta:
        model = Panne
        fields = ['id', 'telephone', 'description']

class OutilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outil
        fields = ['id', 'nom', 'description']

class ReparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reparation
        fields = ['id', 'telephone', 'date_debut', 'date_fin','commentaires', 'telephone_detail' , 'numero_reparation']

class FactureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Facture
        fields = ['id', 'reparation', 'date', 'montant_total', 'client', 'numero_fature', 'numero_reparation']
