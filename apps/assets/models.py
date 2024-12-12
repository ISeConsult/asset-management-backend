from django.db import models
import uuid
from apps.people.models import User
# Create your models here.

class AssetSupplier(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    support_channel = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Supplier"
        verbose_name_plural = "Asset Suppliers"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class AssetCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"
        ordering = ["-created_at"]
    

    def __str__(self):
        return self.name


class AssetStatus(models.Model):
    """
    status_types = (

    ('pending', 'Pending'),
    ('ready-to-deploy', 'Ready to Deploy'),
    ('deployed', 'Deployed'),
    ('archived', 'Archived'),
    ('broken(not-fixable)', 'Broken/Not Fixable'),
    ('lost/stolen', 'Lost/Stolen'),
    ('out for diagnostics', 'Out for Diagnostics'),
    ('out for repair', 'Out for Repair'),
    
    )

    status = ['pending', 'ready-to-deploy', 'deployed', 'archived', 'broken(not-fixable)', 'lost/stolen', 'out for diagnostics', 'out for repair']
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Status"
        verbose_name_plural = "Asset Statuses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Asset(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    serial_no = models.CharField(max_length=255, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to="assets/", null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True, unique=True)
    purchase_date = models.DateField()
    purchase_price = models.FloatField()
    condition = models.CharField(max_length=255, null=True, blank=True,choices=[("new", "New"), ("used", "Used")])
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
    current_assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(AssetSupplier, on_delete=models.CASCADE, null=True, blank=True)
    requestable = models.BooleanField(default=True)
    order_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    

class AssetAssignment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.CharField(max_length=255, null=True, blank=True)
    #status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
    #assigned_at = models.DateField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Assignment"
        verbose_name_plural = "Asset Assignments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} assigned to {self.user.username}"
    

class AssetReturn(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #returned_at = models.DateField() 
    comment = models.TextField(null=True, blank=True)
    #status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
    #assigned_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Return"
        verbose_name_plural = "Asset Returns"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} returned by {self.user.username}"
    

class AssetRequest(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField() 
    status = models.CharField(max_length=255, null=True, blank=True,choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],default="pending")
    comment = models.TextField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    rejection_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Request"
        verbose_name_plural = "Asset Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} requested by {self.user.username}"
    


class MaintenanceRequest(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255,null=True,blank=True,choices=[("pending", "Pending"), ("completed", "Completed"),("in-progress", "In Progress")],default="pending")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maintenance Request"
        verbose_name_plural = "Maintenance Requests"
        ordering = ["-report_date"]

    def __str__(self):
        return f"{self.asset.name} maintenance requested by {self.user.username}"
    

"""
write a signal that listens for a post_save event on asset and add history
"""
class AssetHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, null=True, blank=True,choices=[("assigned", "Assigned"), ("returned", "Returned"), ("replaced", "Replaced"),("repaired", "Repaired")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asset History"
        verbose_name_plural = "Asset Histories"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.asset.name} history"
    

class AssetAssignmentHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, null=True, blank=True,choices=[("assigned", "Assigned"), ("returned", "Returned"), ("replaced", "Replaced"),("repaired", "Repaired")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asset Assignment History"
        verbose_name_plural = "Asset Assignment Histories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.name} assignment history"
    


"""
SOFTWARE ASSET MODELS/Licences 
note: hash all the product keys when storing in db unhash when fetched
"""

class SoftwareCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Software Category"
        verbose_name_plural = "Software Categories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class SoftwareLicences(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    product_key = models.CharField(max_length=355)
    category = models.ForeignKey(SoftwareCategory, on_delete=models.CASCADE)
    # minimum quantity before alert trigger
    company = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    reasignable = models.BooleanField(null=True, blank=True)
    min_qty = models.PositiveIntegerField(null=True, blank=True)
    purchase_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    licenced_to_email = models.EmailField(null=True, blank=True)
    licensed_to_name = models.CharField(max_length=255, null=True, blank=True)
    supplier = models.ForeignKey(AssetSupplier, on_delete=models.CASCADE, null=True, blank=True)
    order_no = models.CharField(max_length=255, null=True, blank=True)
    depreciation = models.CharField(max_length=255, null=True, blank=True,choices=[("do-not-depreciate", "Do not depreciate"), ("computer-depreciation", "Computer Depreciation"), ("phone-depreciation", "phone-depreciation")])
    notes = models.TextField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    available = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Software Licences"
        verbose_name_plural = "Software Licences"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.product_key}"
    

class LicenseCheckout(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    licence = models.ForeignKey(SoftwareLicences, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "License Checkout"
        verbose_name_plural = "License Checkouts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.licence.name} - {self.user.username}"
    

"""
prepare a signal that listens for a post_save event on lisence and add history
"""
class LicenseHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    licence = models.ForeignKey(SoftwareLicences, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, null=True, blank=True,choices=[("assigned", "Assigned"), ("returned", "Returned"), ("replaced", "Replaced"),("repaired", "Repaired")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Licence History"
        verbose_name_plural = "Licence Histories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.licence.name} history"



    
