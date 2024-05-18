from django.db import models
import uuid
import hashlib

def _generate_unique_hash():
    unique_id = uuid.uuid4()
    unique_hash = hashlib.sha256(unique_id.bytes).hexdigest()
    return unique_hash

class Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hash = models.CharField(max_length=64, unique=True, blank=True, editable=False)
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = _generate_unique_hash()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Form {self.id}"

class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    value = models.CharField(max_length=255)
    multi = models.BooleanField(default=False)
    order = models.IntegerField()

    def __str__(self):
        return self.value

class PossibleValue(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='possible_values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Answer(models.Model):
    possible_value = models.ForeignKey(PossibleValue, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f"Answer to {self.possible_value.question.value}: {self.possible_value.value}"
