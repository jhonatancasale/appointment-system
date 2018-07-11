from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.fields import SerializerMethodField
from django.contrib.auth.models import User
from appointment.models import Appointment


class PatientSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = 'full_name email'.split()

    def get_full_name(self, obj: User) -> str:
        return obj.get_full_name()


class AppointmentSerializer(ModelSerializer):
    patient = PatientSerializer(many=False)

    class Meta:
        model = Appointment
        fields = 'id date start_at end_at patient'.split()

    def create(self, validated_data: dict) -> Appointment:
        validate_appointment_datetime(
            validated_data['date'],
            validated_data['start_at'],
            validated_data['end_at']
        )

        patient_email = validated_data.get('patient').get('email')
        validated_data['patient'] = get_patient_by_email(patient_email)

        appointment = Appointment.objects.create(**validated_data)
        appointment.save()

        return appointment

    def update(self, instance: Appointment, validated_data: dict) -> Appointment:
        instance.date = validated_data.get('date', instance.date)

        instance.start_at = validated_data.get('start_at', instance.start_at)
        instance.end_at = validated_data.get('end_at', instance.end_at)

        instance.procedure = validated_data.get('procedure', instance.procedure)

        validate_appointment_datetime(instance.date, instance.start_at,
                                      instance.end_at, update=True)

        patient = validated_data.get('patient')
        if patient is not None:
            instance.patient = get_patient_by_email(patient.get('email'))
        instance.save()

        return instance


def validate_appointment_datetime(date, start_at, end_at, update=False):
    if start_at > end_at:
        raise ValidationError('`start_at` must be lesser than `end_at`.')

    return True


def get_patient_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError('Patient not found.')


class DetailedAppointmentSerializer(ModelSerializer):
    patient = PatientSerializer(many=False)

    class Meta:
        model = Appointment
        fields = ('id', 'date', 'start_at', 'end_at', 'patient', 'procedure')
