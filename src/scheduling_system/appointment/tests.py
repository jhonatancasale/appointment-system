from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from appointment.models import Appointment
import datetime


class AppointmentTests(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.patient = User.objects.create_user(self.username, self.email, self.password)

        self.patient.first_name = "john"
        self.patient.last_name = "snow"
        self.patient.save()

        self.date = datetime.datetime.today().date()
        self.start_at = datetime.datetime.now().time()
        self.end_at = (datetime.datetime.now() + datetime.timedelta(hours=2)).time()
        self.appointment_dict = {'date': self.date,
                                 'start_at': self.start_at,
                                 'end_at': self.end_at,
                                 'patient': self.patient}
        self.appointment = Appointment.objects.create(**self.appointment_dict)

    def create_content_dict(self, content):
        """Returning a copy of `self.appointment_dict` updated with the values
        from the given para `content`"""

        content_dict = self.appointment_dict.copy()
        content_dict.update(content)
        return content_dict

    def ensure_equality(self, response, content, fields='date start_at end_at'.split()):
        """Check if the values returned by the API was the expected values"""

        for key in fields:
            self.assertEqual(response.get(key), str(content.get(key)))

        try:
            email = content.get('patient').email
        except AttributeError:
            email = content.get('patient').get('email')

        self.assertEqual(response.get('patient').get('email'), email)
        self.assertEqual(
            response.get('patient').get('full_name'),
            f'{self.patient.first_name} {self.patient.last_name}'
        )

    def test_list_appointments(self):
        """Checking list() API method"""

        response = self.client.get('/api/appointments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data[0], self.appointment_dict)

    def test_retrieve_appointment(self):
        """Checking retrieve() API method"""

        response = self.client.get('/api/appointments/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_values = response.data
        for key in 'date start_at end_at'.split():
            self.assertEqual(response_values.get(key), str(self.appointment_dict.get(key)))

        self.assertEqual(response_values.get('patient').get('email'), self.email)
        self.assertEqual(
            response_values.get('patient').get('full_name'),
            f'{self.patient.first_name} {self.patient.last_name}'
        )

    def test_post_appointment(self):
        """Checking create() API method"""

        content = {
            "date": self.date + datetime.timedelta(days=1),
            "start_at": "12:00:00",
            "end_at": "13:00:00",
            "patient": {
                "email": self.email
            }
        }

        response = self.client.post('/api/appointments/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ensure_equality(response.data, content)

    def test_post_appointment_with_procedure(self):
        """Checking create() API method (with all possible fields)"""

        content = {
            "date": self.date + datetime.timedelta(days=1),
            "start_at": "12:00:00",
            "end_at": "13:00:00",
            "patient": {
                "email": self.email
            },
            "procedure": "Do this and that and so on"
        }

        response = self.client.post('/api/appointments/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ensure_equality(response.data, content)

    def test_post_appointment_start_at_greater_than_end_at(self):
        """Checking create() API method for a broken known pattern:
        start_at > end_at"""

        content = {
            "date": self.date + datetime.timedelta(days=1),
            "start_at": "13:00:00",
            "end_at": "12:00:00",
            "patient": {
                "email": self.email
            }
        }

        response = self.client.post('/api/appointments/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_appointment(self):
        """Checking update() API method"""

        content = {
            "date": self.date + datetime.timedelta(days=2),
            "start_at": "10:00:00",
            "end_at": "12:00:00",
            "patient": {
                "email": self.email
            }
        }

        response = self.client.put('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, content)

    def test_put_appointment_with_procedure(self):
        """Checking update() API method (with all possible values)"""

        content = {
            "date": self.date + datetime.timedelta(days=2),
            "start_at": "10:00:00",
            "end_at": "12:00:00",
            "patient": {
                "email": self.email
            },
            "procedure": "Do this and bla bla bla"
        }

        response = self.client.put('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, content)

    def test_patch_appointment_date(self):
        """Checking partial_update() API method changing the date"""

        content = {
            "date": self.date + datetime.timedelta(days=10),
        }

        response = self.client.patch('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, self.create_content_dict(content))

    def test_patch_appointment_start_at(self):
        """Checking partial_update() API method changing the start_at"""

        content = {
            "start_at": "13:00:00"
        }

        response = self.client.patch('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, self.create_content_dict(content))

    def test_patch_appointment_end_at(self):
        """Checking partial_update() API method changing the end_at"""

        content = {
            "end_at": "18:00:00",
        }

        response = self.client.patch('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, self.create_content_dict(content))

    def test_patch_appointment_procedure(self):
        """Checking partial_update() API method changing the procedure"""

        content = {
            "procedure": "Something",
        }

        response = self.client.patch('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ensure_equality(response.data, self.create_content_dict(content))

    def test_patch_appointment_patient(self):
        """Checking partial_update() API method changing the patient"""

        username = "peter"
        email = "peter@gunn.com"
        password = "maybe_you_know_something"
        patient = User.objects.create_user(username, email, password)
        patient.save()

        content = {
            "patient": {
                "email": email
            }
        }

        response = self.client.patch('/api/appointments/1/', data=content, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('patient').get('email'), email)

    def test_delete_appointment(self):
        """Checking delete() API method"""

        response = self.client.delete('/api/appointments/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
