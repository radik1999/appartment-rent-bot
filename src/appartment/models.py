from django.db import models


class AppartmentOwner(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=False, unique=True)


class Appartment(models.Model):
    room_number = models.PositiveIntegerField()
    cost_per_month = models.PositiveIntegerField()
    owner = models.ForeignKey(AppartmentOwner, related_name="appartments", on_delete=models.CASCADE)

    @classmethod
    def get_formatted_appartments(cls):
        appartments = cls.objects.select_related("owner").all()
        return map(cls.format_appartment, appartments)
    
    @staticmethod
    def format_appartment(appartment: "Appartment") -> str:
        return (
            f"Apparment with {appartment.room_number} rooms\n"
            f"Cost {appartment.cost_per_month}$ per month\n"
            f"Appartment owner is {appartment.owner.first_name} {appartment.owner.last_name}\n"
            f"You can contanct with him via this phone number {appartment.owner.phone_number}"
        )