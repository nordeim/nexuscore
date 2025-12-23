"""
NexusCore Constants
Singapore-specific configuration values
"""
from decimal import Decimal

# =============================================================================
# TIMEZONE & LOCALE (Singapore)
# =============================================================================
SINGAPORE_TIMEZONE = 'Asia/Singapore'
DEFAULT_LOCALE = 'en-SG'

# =============================================================================
# CURRENCY
# =============================================================================
DEFAULT_CURRENCY = 'SGD'
CURRENCY_DECIMAL_PLACES = 2

# =============================================================================
# GST CONFIGURATION (Singapore IRAS)
# =============================================================================
GST_RATE = Decimal('0.0900')  # 9% as of 2024
GST_RATE_DISPLAY = '9%'
GST_REGISTRATION_THRESHOLD = 1_000_000  # SGD 1 million

# IRAS Transaction Codes
IRAS_TRANSACTION_CODES = {
    'SR': 'Standard Rate',
    'ZR': 'Zero Rate',
    'OS': 'Out of Scope',
    'TX': 'Taxable Supply',
}

# =============================================================================
# PDPA COMPLIANCE (Singapore)
# =============================================================================
DSAR_SLA_HOURS = 72  # 72-hour SLA for DSAR requests
PDPA_DATA_RETENTION_DAYS = 2555  # ~7 years for financial records
PDPA_EXPORT_EXPIRY_HOURS = 168  # 7 days for data export links

# =============================================================================
# IDEMPOTENCY
# =============================================================================
IDEMPOTENCY_KEY_HEADER = 'Idempotency-Key'
IDEMPOTENCY_EXPIRY_HOURS = 24

# =============================================================================
# ORGANIZATION ROLES
# =============================================================================
ORGANIZATION_ROLES = {
    'owner': 'Owner',
    'admin': 'Administrator',
    'member': 'Member',
    'viewer': 'Viewer',
}

# =============================================================================
# SUBSCRIPTION STATUS
# =============================================================================
SUBSCRIPTION_STATUS = {
    'trialing': 'Trialing',
    'active': 'Active',
    'past_due': 'Past Due',
    'canceled': 'Canceled',
    'unpaid': 'Unpaid',
}

# =============================================================================
# INVOICE STATUS
# =============================================================================
INVOICE_STATUS = {
    'draft': 'Draft',
    'open': 'Open',
    'paid': 'Paid',
    'void': 'Void',
    'uncollectible': 'Uncollectible',
}

# =============================================================================
# LEAD STATUS
# =============================================================================
LEAD_STATUS = {
    'new': 'New',
    'contacted': 'Contacted',
    'qualified': 'Qualified',
    'proposal': 'Proposal',
    'negotiation': 'Negotiation',
    'won': 'Won',
    'lost': 'Lost',
}

# =============================================================================
# DSAR REQUEST TYPES
# =============================================================================
DSAR_REQUEST_TYPES = {
    'access': 'Data Access',
    'export': 'Data Export',
    'delete': 'Data Deletion',
    'correct': 'Data Correction',
}

DSAR_STATUS = {
    'pending': 'Pending Verification',
    'verified': 'Verified',
    'processing': 'Processing',
    'completed': 'Completed',
    'rejected': 'Rejected',
}
