from rest_framework import serializers

from apps.plans.models import Plan, PlanTableRow, PlanType


class PlanTableRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanTableRow
        fields = [
            "id",
            "plan",
            "label",
            "duration_years",
            "deposit_amount",
            "premium_amount",
            "maturity_amount",
            "interest_rate",
            "fund_value",
            "surrender_value",
            "family_protection",
            "monthly_income",
            "sort_order",
            "metadata",
            "is_active",
        ]


class PlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "slug",
            "plan_type",
            "short_description",
            "benefits",
            "is_featured",
            "sort_order",
        ]


class PlanDetailSerializer(serializers.ModelSerializer):
    table_rows = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "slug",
            "plan_type",
            "short_description",
            "description",
            "benefits",
            "terms_conditions",
            "is_featured",
            "sort_order",
            "table_rows",
        ]

    def get_table_rows(self, obj):
        rows = obj.table_rows.filter(is_active=True)
        return PlanTableRowSerializer(rows, many=True).data


class PlanAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "slug",
            "plan_type",
            "short_description",
            "description",
            "benefits",
            "terms_conditions",
            "is_featured",
            "sort_order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class CalculatorRequestSerializer(serializers.Serializer):
    plan_type = serializers.ChoiceField(choices=PlanType.choices, default=PlanType.RD)
    monthly_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=1)
    duration_years = serializers.IntegerField(min_value=1, max_value=50)


class CalculatorResponseSerializer(serializers.Serializer):
    total_deposit = serializers.DecimalField(max_digits=16, decimal_places=2)
    estimated_maturity = serializers.DecimalField(max_digits=16, decimal_places=2)
    estimated_benefit = serializers.DecimalField(max_digits=16, decimal_places=2)
    disclaimer = serializers.CharField()
