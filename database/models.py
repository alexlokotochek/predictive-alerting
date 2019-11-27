import datetime
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Float, DateTime,
)
from sqlalchemy.orm import relationship
from database import Base


class AlertType(Base):
    """Table with types of alerts. Used by alert_sender service
    to identify what to do in case if alert is triggered.
    """
    __tablename__ = "alerts_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    error_value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Action to perform if alert of that type is triggered.
    action = Column(String)  # send_message
    destination = Column(String)  # url to call or slack channel


class Metric(Base):
    """Table with metrics. Used by task_runner service to
    identify which tasks should be run and what alert type 
    should be triggered in case if error reached 
    predicted_error_alert_threshold.
    """
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    alert_type_id = Column(Integer, ForeignKey("alert_types.id"))

    # How often metrics are pulled
    prediction_freq_s = Column(Float, default=60.)
    # What period of metric time series should be analyzed
    predicted_analysis_period_s = Column(Float, default=600.)
    # Lower bound for error to trigger an alert
    predicted_error_alert_threshold = Column(Float, default=0.1)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_predicted_date = Column(DateTime, default=datetime.datetime.utcnow)


class Alert(Base):
    """Table with alerts. Alert is created by a task_runner service.
    Alert_sender service aquires lock on that table, grabs alerts, 
    deletes them, releases the table and sends according to 
    alert types.
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("metrics.id"))

    description = Column(String)
    error_value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
