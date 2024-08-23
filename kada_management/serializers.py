from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Client, Telephone, Diagnostic, Reparation, Facture, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email','nom','prenom','is_active', 'is_staff', 'is_superuser','is_commercial','is_technician', 'password']
        extra_kwargs = {'password': {
                'write_only': True,
                'required': False,
            }}

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        token['is_commercial'] = user.is_commercial
        token['is_technician'] = user.is_technician
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff

        return token


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
    user = CustomUserSerializer(read_only=True)
    
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
            'telephone_name',
            'diagnostic_type',
            'numero_diagnostic',
            'user',
            'owner'
        ]
        read_only_fields = ['id', 'date']


class ReparationSerializer(serializers.ModelSerializer):
    initial_diagnostic_id = serializers.PrimaryKeyRelatedField(queryset=Diagnostic.objects.all(), source='initial_diagnostic', required=True)
    final_diagnostic_id = serializers.PrimaryKeyRelatedField(queryset=Diagnostic.objects.all(), source='final_diagnostic',required=False, allow_null=True)
    technician_diagnostic_id = serializers.PrimaryKeyRelatedField(queryset=Diagnostic.objects.all(), source='technician_diagnostic',required=False, allow_null=True)
    telephone_id = serializers.PrimaryKeyRelatedField(queryset=Telephone.objects.all(), source='telephone', required=True)
    technician_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='telephone', required=True)

    initial_diagnostic = DiagnosticSerializer(read_only=True)
    final_diagnostic = DiagnosticSerializer(read_only=True)
    technician_diagnostic = DiagnosticSerializer(read_only=True)
    telephone = TelephoneSerializer(read_only=True)
    technician = CustomUserSerializer(read_only=True)

    date_debut = serializers.DateTimeField(allow_null=True, required=False)
    date_fin = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Reparation
        fields = ['id', 
                  'telephone', 
                  'telephone_id',
                  'date_debut', 
                  'date_fin',
                  'commentaires', 
                  'telephone_detail' , 
                  'numero_reparation',
                  'commercial', 
                  'technician', 
                  'technician_id',
                  'initial_diagnostic', 
                  'initial_diagnostic_id', 
                  'final_diagnostic', 
                  'final_diagnostic_id',
                  'technician_diagnostic', 
                  'technician_diagnostic_id',
                  'status']
        
        extra_kwargs = {
            'date_debut': {
                'required': False,
            },
            'date_fin': {
                'required': False,
            }
        }
    

class FactureSerializer(serializers.ModelSerializer):
    reparation_id = serializers.PrimaryKeyRelatedField(queryset=Reparation.objects.all(), source='reparation',required=False, allow_null=True)
    reparation = ReparationSerializer(read_only=True)
    class Meta:
        model = Facture
        fields = ['id', 'reparation', 'date', 'montant_total', 'client', 'numero_fature', 
                  'numero_reparation','reparation_id', 'numero_telephone']


