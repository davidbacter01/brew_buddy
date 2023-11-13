from django.db import models
from django.conf import settings
from uuid import uuid4
from web.exceptions import InvalidOperationException
from django.contrib.auth.models import AbstractUser, Group, Permission
import io
import segno


def generate_uuid_str() -> str:
    """Generates a unique identifier and returns it as a string"""
    uuid_4 = uuid4()
    return str(uuid_4)


def generate_qr(to_encode: str, kind='png', dark='#00008b', light: str | None = None, scale=3) -> io.BytesIO:
    """
    Generates a QR code from the given string and kind and returns a binary representation (BytesIO)
    of the QR code
    """
    out = io.BytesIO()
    qr = segno.make(to_encode)
    qr.save(out, kind=kind, dark=dark, light=light, scale=scale)
    return out


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)


class UOMCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)

    def __str__(self)-> str:
        return self.name


class UnitOfMeasure(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        UOMCategory, blank=False, null=True, on_delete=models.SET_NULL)
    sub_unit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='supra_unit')
    sub_unit_multiplier = models.FloatField(blank=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Ingredient(BaseModel):
    name = models.CharField(max_length=50)
    unit_of_measurement = models.ForeignKey(
        UnitOfMeasure, blank=False, null=True, on_delete=models.SET_NULL)
    note = models.TextField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f'<Ingredient: {str(self.unit_of_measurement)} {self.name}>'
    

class ReciepeLine(BaseModel):
    rec_ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    related_reciepe = models.ForeignKey('Reciepe', on_delete=models.CASCADE, related_name='reciepe_lines')
    note = models.TextField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f'{str(self.rec_ingredient)} {self.quantity}>'


class Reciepe(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    note = models.TextField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f'<Reciepe: {self.name}>'


class BrewBatch(BaseModel):
    related_reciepe = models.ForeignKey(
        Reciepe, on_delete=models.SET_NULL, null=True, blank=True)
    volume_quantity = models.FloatField()
    volume_uom = models.ForeignKey(
        UnitOfMeasure, blank=False, null=True, on_delete=models.SET_NULL)
    datetime_start = models.DateTimeField(auto_now=True)
    date_end = models.DateField(blank=True)
    uid = models.CharField(max_length=50, default=generate_uuid_str)

    def __str__(self) -> str:
        return f'<BrewBatch: {self.reciepe.name}, {str(self.datetime_start)}>'

    def get_qr(self) -> io.BytesIO:
        return generate_qr(self.uid)

    def compute_qty_by_reciepe(self, reciepe: Reciepe | None = None):
        used_reciepe = reciepe and reciepe or self.reciepe
        if not used_reciepe:
            raise InvalidOperationException(
                "No reciepe specified to compute quantities.")
        # todo: implement this
        pass


class DensityReading(BaseModel):
    read_value = models.FloatField()
    note = models.TextField(max_length=255)
    brew_batch = models.ForeignKey(BrewBatch, related_name='density_readings', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'<Reading: {self.read_value}, {str(self.date_time)}>'
