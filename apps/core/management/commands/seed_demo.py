"""Seed demo/reference data matching the Phase 1 frontend content.

Usage: python manage.py seed_demo
Idempotent — safe to run multiple times.
"""

from django.core.management.base import BaseCommand

from apps.core.models import WebsiteSettings
from apps.content.models import ContentType, Event, LegalDocument
from apps.media_library.models import GalleryCategory, Video, VideoType
from apps.plans.models import Plan, PlanTableRow, PlanType

RD_ROWS = [
    ("6 years", 6, 6, 72000, 85140),
    ("8 years", 8, 8, 96000, 127040),
    ("10 years", 10, 10, 120000, 180500),
    ("12 years", 12, 12, 144000, 248500),
    ("15 years", 15, 13, 180000, 356600),
    ("18 years", 18, 14, 216000, 489540),
    ("21 years", 21, 15, 252000, 650600),
    ("24 years", 24, 16, 288000, 843020),
]


class Command(BaseCommand):
    help = "Seed reference data for local development."

    def handle(self, *args, **options):
        self._settings()
        self._plans()
        self._legal()
        self._events()
        self._gallery_and_videos()
        self.stdout.write(self.style.SUCCESS("Seed complete."))

    def _settings(self):
        s = WebsiteSettings.load()
        s.site_name = "Aaradhana Bachat"
        s.primary_phone = "+91 98980 98744"
        s.address = "Sai Elegance, Second Floor, Above Axis Bank, Kalikund, Dholka"
        s.office_hours = ""
        s.save()

    def _plans(self):
        rd, _ = Plan.objects.update_or_create(
            slug="rd-plan",
            defaults=dict(
                name="RD Plan",
                plan_type=PlanType.RD,
                short_description="Save a fixed amount every month and earn from 6% up to 16%.",
                benefits=["Tenures from 6 to 24 years", "Interest rates from 6% up to 16%"],
                is_featured=True,
                sort_order=1,
            ),
        )
        rd.table_rows.all().delete()
        for i, (label, years, rate, deposit, maturity) in enumerate(RD_ROWS):
            PlanTableRow.objects.create(
                plan=rd,
                label=label,
                duration_years=years,
                interest_rate=rate,
                deposit_amount=deposit,
                maturity_amount=maturity,
                sort_order=i,
            )
        Plan.objects.update_or_create(
            slug="term-plan",
            defaults=dict(
                name="Term Plan",
                plan_type=PlanType.TERM,
                short_description="A single-premium plan combining fund growth and family protection.",
                benefits=["Family protection cover", "Growing fund value with surrender value"],
                sort_order=2,
            ),
        )

    def _legal(self):
        docs = [
            ("Society Registration Certificate", "Registration"),
            ("Rules & Bye-laws", "Governance"),
            ("Member Terms & Conditions", "Member Documents"),
        ]
        for i, (title, category) in enumerate(docs):
            LegalDocument.objects.update_or_create(
                slug=title.lower().replace(" ", "-").replace("&", "and"),
                defaults=dict(title=title, category=category, sort_order=i),
            )

    def _events(self):
        events = [
            ("Annual General Meeting 2026", ContentType.EVENT, "2026-08-15"),
            ("Financial Literacy Camp", ContentType.EVENT, "2026-07-20"),
            ("New Savings Plan Launch", ContentType.NEWS, "2026-07-05"),
        ]
        for i, (title, ctype, date) in enumerate(events):
            Event.objects.update_or_create(
                slug=title.lower().replace(" ", "-"),
                defaults=dict(
                    title=title,
                    type=ctype,
                    short_description=f"{title} — details coming soon.",
                    content=f"Full details for {title}.",
                    event_date=date,
                    published_date=date,
                    sort_order=i,
                ),
            )

    def _gallery_and_videos(self):
        for i, name in enumerate(["Events", "Community", "Workshops", "Achievements"]):
            GalleryCategory.objects.update_or_create(
                slug=name.lower(), defaults=dict(name=name, sort_order=i)
            )
        videos = [
            ("Welcome to Aaradhana Bachat", "aqz-KE-bpKQ"),
            ("How Our Savings Plans Work", "ScMzIvxBSi4"),
        ]
        for i, (title, yid) in enumerate(videos):
            Video.objects.update_or_create(
                title=title,
                defaults=dict(
                    video_type=VideoType.YOUTUBE,
                    youtube_url=f"https://www.youtube.com/watch?v={yid}",
                    sort_order=i,
                ),
            )
