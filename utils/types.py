from dataclasses import dataclass, field
from typing import Optional, Dict
from datetime import datetime
import uuid

@dataclass
class PaymentEvent:
    id: str
    issuer: str
    amount: float
    status: str
    error_code: Optional[str]
    latency_ms: int
    created_at: str
    metadata: Dict = field(default_factory=dict)

    @staticmethod
    def new(issuer, amount, status, error_code, latency):
        return PaymentEvent(
            id=str(uuid.uuid4()),
            issuer=issuer,
            amount=amount,
            status=status,
            error_code=error_code,
            latency_ms=latency,
            created_at=datetime.utcnow().isoformat()
        )
