from django.db import models
from studio_profiles.models import Horse, Owner, Trainer


class MediaAsset(models.Model):
    class Kind(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        EMBED = "EMBED", "Embed"

    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.IMAGE)
    url = models.URLField(blank=True)
    caption = models.CharField(max_length=500, blank=True)
    credit = models.CharField(max_length=255, blank=True)
    source_update = models.ForeignKey(
        "Update",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media_library_entries",
    )
    published_date = models.DateField(null=True, blank=True)
    public_url = models.URLField(blank=True)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Media Library"
        verbose_name_plural = "Media Library"


class Update(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        REVIEW = "REVIEW", "Review"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    class UpdateType(models.TextChoices):
        TRAINER_UPDATE = "TRAINER_UPDATE", "Trainer Update"
        RACE_PREVIEW = "RACE_PREVIEW", "Race Preview"
        RACE_RESULT = "RACE_RESULT", "Race Result"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    update_type = models.CharField(
        max_length=20,
        choices=UpdateType.choices,
        default=UpdateType.TRAINER_UPDATE,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    primary_horse = models.ForeignKey(
        Horse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_updates",
    )
    horses = models.ManyToManyField(Horse, related_name="updates", blank=True)
    trainers = models.ManyToManyField(Trainer, related_name="updates", blank=True)
    owners = models.ManyToManyField(Owner, related_name="updates", blank=True)
    jockey = models.CharField(max_length=255, blank=True)
    race_track = models.CharField(max_length=255, blank=True)
    race_date = models.DateField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    public_url = models.URLField(blank=True)
    rendered_html = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Content Library"
        verbose_name_plural = "Content Library"


class ContentBlock(models.Model):
    class BlockType(models.TextChoices):
        HEADING = "HEADING", "Heading"
        SUBHEADING = "SUBHEADING", "Subheading"
        BODY = "BODY", "Body"
        BULLETS = "BULLETS", "Bullets"
        GREY_BOX = "GREY_BOX", "Grey Box"

    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name="blocks")
    order = models.PositiveIntegerField(default=0)
    block_type = models.CharField(max_length=20, choices=BlockType.choices)
    text = models.TextField(blank=True)
    bullets = models.TextField(blank=True)
    media = models.ForeignKey(
        MediaAsset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blocks",
    )
    quote = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    media_portrait = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.update.title} #{self.order} {self.block_type}"

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Block Item"
        verbose_name_plural = "Block Items"
