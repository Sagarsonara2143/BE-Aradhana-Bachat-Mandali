from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.permissions import IsAdminRole
from apps.plans.calculator import calculate_maturity
from apps.plans.models import Plan, PlanTableRow
from apps.plans.serializers import (
    CalculatorRequestSerializer,
    CalculatorResponseSerializer,
    PlanAdminSerializer,
    PlanDetailSerializer,
    PlanListSerializer,
    PlanTableRowSerializer,
)


class PublicPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Public, read-only plans API (active plans only)."""

    permission_classes = [AllowAny]
    lookup_field = "slug"
    queryset = Plan.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["plan_type", "is_featured"]

    def get_serializer_class(self):
        return PlanListSerializer if self.action == "list" else PlanDetailSerializer

    @action(detail=True, methods=["get"])
    def tables(self, request, slug=None):
        plan = self.get_object()
        rows = plan.table_rows.filter(is_active=True)
        return Response(PlanTableRowSerializer(rows, many=True).data)

    @extend_schema(request=CalculatorRequestSerializer, responses=CalculatorResponseSerializer)
    @action(detail=False, methods=["post"])
    def calculate(self, request):
        serializer = CalculatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = calculate_maturity(**serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)


class AdminPlanViewSet(viewsets.ModelViewSet):
    """Admin CRUD for plans."""

    permission_classes = [IsAdminRole]
    queryset = Plan.objects.all()
    serializer_class = PlanAdminSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["plan_type", "is_featured", "is_active"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="table-rows")
    def add_table_row(self, request, pk=None):
        plan = self.get_object()
        serializer = PlanTableRowSerializer(data={**request.data, "plan": plan.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user, updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminPlanTableRowViewSet(viewsets.ModelViewSet):
    """Admin update/delete for individual plan table rows."""

    permission_classes = [IsAdminRole]
    queryset = PlanTableRow.objects.all()
    serializer_class = PlanTableRowSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
