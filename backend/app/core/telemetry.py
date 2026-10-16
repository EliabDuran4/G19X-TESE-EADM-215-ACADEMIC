from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import View, ExplicitBucketHistogramAggregation
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.config import settings


def setup_telemetry(app):
    resource = Resource.create({"service.name": settings.otel_service_name})

    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(trace_provider)

    metric_exporter = OTLPMetricExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)

    decision_view = View(
        instrument_name="document_decision_duration_seconds",
        aggregation=ExplicitBucketHistogramAggregation(
            [60, 300, 900, 3600, 14400, 43200, 86400, 259200, 604800]
        ),
    )

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
        views=[decision_view],
    )
    metrics.set_meter_provider(meter_provider)

    FastAPIInstrumentor.instrument_app(app)