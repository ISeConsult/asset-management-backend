from django.db import models
import uuid
# Create your models here.


class LicenseCategoryTypes(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'License Category Type'
        verbose_name_plural = 'License Category Types'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class LicenseCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    category_type = models.ForeignKey(LicenseCategoryTypes,on_delete=models.CASCADE)
    note = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'License Category'
        verbose_name_plural = 'License Categories'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class License(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    product_key = models.CharField(max_length=200)
    depriciation = models.CharField(max_length=120,null=True,blank=True)
    category = models.ForeignKey(LicenseCategory,on_delete=models.CASCADE)
    company = models.ForeignKey("assets.Company",on_delete=models.CASCADE,null=True,blank=True)
    manufacturer = models.ForeignKey("assets.AssetManufacturer",on_delete=models.CASCADE)
    order_number = models.CharField(max_length=120)
    licensed_to_email = models.EmailField(null=True,blank=True)
    licensed_to = models.ForeignKey("people.User",on_delete=models.CASCADE,null=True,blank=True)
    purchase_cost = models.PositiveIntegerField(default=0)
    termination_date = models.DateField(null=True,blank=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=120,default="checked_in",choices=(("checked_in","Checked In"),("checked_out","Checked Out"),("expired","Expired")))
    expiry_date = models.DateField(null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    location = models.ForeignKey("assets.AssetLocation",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    


class LicenseCheckOut(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE,related_name='license_checkout_user')
    checkout_by = models.ForeignKey("people.User", on_delete=models.CASCADE,related_name='license_checkout_checkout_by')
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'License CheckOut'
        verbose_name_plural = 'License CheckOuts'
        ordering = ['-created_at']

    def __str__(self):
        return self.license.name
    

class LicenseHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE,related_name='license_history_user')
    action = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'License History'
        verbose_name_plural = 'License Histories'
        ordering = ['-created_at']

    def __str__(self):
        return self.license.name


