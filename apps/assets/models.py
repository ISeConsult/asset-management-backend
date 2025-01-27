from django.db import models
import uuid
from django.utils.translation import gettext_lazy as t

class AssetModelCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Model Category"
        verbose_name_plural = "Asset Model Categories"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class AssetManufacturer(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    web_url = models.URLField(null=True, blank=True)
    support_url = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    image = models.ImageField(upload_to="manufacturers/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Manufacturer"
        verbose_name_plural = "Asset Manufacturers"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class AssetModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    model_no = models.CharField(max_length=120, null=True, blank=True)
    fieldset = models.TextField(null=True, blank=True)
    category = models.ForeignKey(AssetModelCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/", null=True, blank=True)
    manufacturer = models.ForeignKey(AssetManufacturer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Model"
        verbose_name_plural = "Asset Models"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name




class AssetLocation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    location_name = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    location_currency = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to="locations/", null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Location"
        verbose_name_plural = "Asset Locations"
        ordering = ["-created_at"]

    def __str__(self):
        return self.location_name


class AssetCategoryTypes(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Category Type"
        verbose_name_plural = "Asset Category Types"
        ordering = ["-created_at"]


class AssetCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    asset_type = models.ForeignKey(
        AssetCategoryTypes, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=0)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Company(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company_name = models.CharField(max_length=120)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="companies/", null=True, blank=True)
    company_phone = models.CharField(max_length=120)
    company_mail = models.EmailField()
    website = models.URLField(null=True, blank=True)
    fax = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.company_name


class AssetSupplier(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to="suppliers/", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Supplier"
        verbose_name_plural = "Asset Suppliers"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Asset(models.Model):
    class AssetStatus(models.TextChoices):
        PENDING = 'pending',t('Pending')
        CHECKED_IN = 'checked_in',t('Checked In')
        CHECKED_OUT = 'checked_out',t('Checked Out')
        IN_REPAIR = 'in_repair',t('In Repair')

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    asset_tag = models.CharField(max_length=120)
    serial_no = models.CharField(max_length=120)
    asset_model = models.ForeignKey(AssetModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default=AssetStatus.PENDING,choices=AssetStatus.choices)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    purchase_cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="assets/", null=True, blank=True)
    order_number = models.CharField(max_length=120)
    supplier = models.ForeignKey(AssetSupplier, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(
        AssetManufacturer, on_delete=models.CASCADE, null=True, blank=True
    )
    current_assignee = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, null=True, blank=True
    )
    purchase_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class AssetRequest(models.Model):
    class AssetRequestStatus(models.TextChoices):
        PENDING = 'pending',t('pending')
        APPROVED = 'approved',t('Approved')
        REJECTED = 'rejected',t('Rejected')
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)
    request_date = models.DateField()
    user = models.ForeignKey(
        "people.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="asset_request_user",
    )
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    expected_checkin_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=120, default=AssetRequestStatus.PENDING,choices=AssetRequestStatus.choices)
    submitted_by = models.ForeignKey("people.User", on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Request"
        verbose_name_plural = "Asset Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return self.asset.name


class AssetCheckIn(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, null=True, blank=True
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset CheckIn"
        verbose_name_plural = "Asset CheckIns"
        ordering = ["-created_at"]

    # def __str__(self):
    #     return self.name

    # def save(self, *args, **kwargs):
    #     if self.status.name == "checked_in":
    #         self.asset.status = self.status.name
    #     return super().save(*args, **kwargs)


class AssetCheckOut(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset_request = models.ForeignKey(
        AssetRequest, on_delete=models.CASCADE, null=True, blank=True
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, related_name="asset_checkout_user"
    )
    checkout_by = models.ForeignKey(
        "people.User",
        on_delete=models.CASCADE,
        related_name="asset_checkout_checkout_by",
    )
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset CheckOut"
        verbose_name_plural = "Asset CheckOuts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.asset.name


class AssetReturn(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    return_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Return"
        verbose_name_plural = "Asset Returns"
        ordering = ["-created_at"]

    def __str__(self):
        return self.asset.name


class AssetMaintenanceRequest(models.Model):
    class MaintenanceStatuses(models.TextChoices):
        PENDING = 'pending',t('Pending')
        COMPLETED = 'completed',t('Completed')


    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE)
    request_date = models.DateField()
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=120, default=MaintenanceStatuses.PENDING,choices=MaintenanceStatuses.choices)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AssetMaintenanceRequest"
        verbose_name_plural = "AssetMaintenanceRequests"
        ordering = ["-created_at"]

    def __str__(self):
        return self.asset.name


class AssetAudit(models.Model):
    class AuditStatus(models.TextChoices):
        PENDING = 'pending',t('Pending')
        COMPLETED = 'completed',t('Completed')

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default=AuditStatus.PENDING,choices=AuditStatus.choices)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Asset Audit'
        verbose_name_plural = 'Audit Audits'
        ordering = ['-created_at']




class Components(models.Model):
        
    class ComponentStatus(models.TextChoices):
        PENDING = 'pending',t('Pending')
        CHECKED_IN = 'checked_in',t('Checked In')
        CHECKED_OUT = 'checked_out',t('Checked Out')
        IN_REPAIR = 'in_repair',t('In Repair')


    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    order_number = models.CharField(max_length=120)
    item_number = models.CharField(max_length=120,null=True, blank=True)
    model = models.ForeignKey(AssetModel, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(AssetManufacturer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    purchase_cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="components/", null=True, blank=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=50,default=ComponentStatus.PENDING,choices=ComponentStatus.choices)
    supplier = models.ForeignKey(AssetSupplier, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    current_assignee = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ["-created_at"]


class ComponentCheckIn(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, null=True, blank=True
    )
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Component CheckIn"
        verbose_name_plural = "Component CheckIns"
        ordering = ["-created_at"]

    def __str__(self):
        return self.component.name
    


class ComponentRequest(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    request_date = models.DateField()
    user = models.ForeignKey("people.User",on_delete=models.CASCADE)
    status = models.CharField(max_length=120,default="pending",choices=(("pending","Pending"),("approved","Approved"),("rejected","Rejected")))
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Component Request"
        verbose_name_plural = "Component Requests"
        ordering = ["-created_at"]


class ComponentCheckOut(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    component_request = models.ForeignKey(
        ComponentRequest, on_delete=models.CASCADE, null=True, blank=True
    )
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    user = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, related_name="component_checkout_user"
    )
    checkout_by = models.ForeignKey(
        "people.User",
        on_delete=models.CASCADE,
        related_name="component_checkout_checkout_by",
    )
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Component CheckOut"
        verbose_name_plural = "Component CheckOuts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.component.name



class AssetsHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE, related_name='asset_history_user')
    action = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Asset History'
        verbose_name_plural = 'Asset Histories'
        ordering = ['-created_at']

    def __str__(self):
        return self.asset.name
    

class ComponentHistory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE, related_name='component_history_user')
    action = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Component History'
        verbose_name_plural = 'Component Histories'
        ordering = ['-created_at']

    def __str__(self):
        return self.component.name