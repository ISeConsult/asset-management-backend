from django.db import models
import uuid


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
    web_url = models.URLField(null=True, blank=True)
    support_url = models.CharField(max_length=120)
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
    category = models.ForeignKey(AssetModelCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/")
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


class AssetStatus(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset Status"
        verbose_name_plural = "Asset Statuses"
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


class AssetCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120)
    asset_tag = models.CharField(max_length=120)
    serial_no = models.CharField(max_length=120)
    asset_model = models.ForeignKey(AssetModel, on_delete=models.CASCADE)
    status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    purchase_cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="assets/", null=True, blank=True)
    order_number = models.CharField(max_length=120)
    supplier = models.ForeignKey(AssetSupplier, on_delete=models.CASCADE)
    current_assignee = models.ForeignKey("people.User", on_delete=models.CASCADE)
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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)
    request_date = models.DateField()
    user = models.ForeignKey(
        "people.User", on_delete=models.CASCADE, null=True, blank=True
    )
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    expected_checkin_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=120, blank=True, null=True)
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
    asset_request = models.ForeignKey(AssetRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
    location = models.ForeignKey(AssetLocation, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset CheckIn"
        verbose_name_plural = "Asset CheckIns"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status.name == "deployed":
            self.asset_request.status = self.status.name
            self.asset_request.expected_checkin_date = self.checkin_date
        return super().save(*args, **kwargs)


class AssetReturn(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE)
    status = models.ForeignKey(AssetStatus, on_delete=models.CASCADE)
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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey("people.User", on_delete=models.CASCADE)
    request_date = models.DateField()
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
