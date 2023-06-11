from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Therapist(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    Therapist_link= models.CharField(max_length=200)

    def __str__(self):
        return self.username.username

class TreatmentPlan(models.Model):
    ID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    Psychological_symptoms = models.TextField()
    Psychological_treatments = models.TextField()

    def __str__(self):
        return self.title

class Treatment(models.Model):
    plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    goals = models.TextField()
    objectives = models.TextField()
    interventions = models.TextField()
    progress_notes = models.TextField()

    def __str__(self):
        return f"Treatment {self.id}"

class SessionTreatment(models.Model):
    ID = models.AutoField(primary_key=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    datetime_session = models.DateTimeField()
    progress = models.TextField()
    assessment_scores = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Session Treatment {self.ID}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    notes = models.TextField()
    datetimeApp = models.DateTimeField()
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('D', 'Done'),
        ('C', 'Canceled'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment {self.id}"

class Medication(models.Model):
    ID = models.AutoField(primary_key=True)
    medication_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('L', 'Liquid'),
        ('T', 'Tablet'),
        ('C', 'Capsule'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.medication_name

class MedicationTreatment(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    prescribing_therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)

    def __str__(self):
        return f"Medication Treatment {self.id}"

class ChatHistory(models.Model):
    IDchat = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user_message = models.TextField()
    chatbot_responses = models.TextField()
    e_counselling = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat History {self.IDchat}"

    

