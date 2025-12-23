/**
 * TypeScript Model Types
 * Match backend Django models exactly
 */

// ============================================================================
// User & Auth Models
// ============================================================================

export interface User {
    id: string;
    email: string;
    name: string;
    company?: string;
    timezone: string;
    is_verified: boolean;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface TokenResponse {
    access: string;
    refresh: string;
}

// ============================================================================
// Organization Models
// ============================================================================

export interface Organization {
    id: string;
    name: string;
    slug: string;
    uen: string;
    is_gst_registered: boolean;
    gst_reg_no?: string;
    billing_email?: string;
    billing_address?: Record<string, unknown>;
    org_timezone: string;
    org_settings: Record<string, unknown>;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export type MemberRole = 'owner' | 'admin' | 'member' | 'viewer';

export interface OrganizationMembership {
    id: string;
    organization: string;
    user: string;
    role: MemberRole;
    permissions: string[];
    invited_by?: string;
    joined_at: string;
    is_active: boolean;
}

// ============================================================================
// Subscription Models
// ============================================================================

export type BillingPeriod = 'monthly' | 'yearly';

export interface Plan {
    id: string;
    sku: string;
    name: string;
    description: string;
    billing_period: BillingPeriod;
    amount_cents: number;
    currency: string;
    features: Record<string, unknown>;
    limits: Record<string, unknown>;
    is_active: boolean;
    is_visible: boolean;
    display_order: number;
    stripe_price_id?: string;
    stripe_product_id?: string;
}

export type SubscriptionStatus = 'trialing' | 'active' | 'past_due' | 'canceled' | 'unpaid';

export interface Subscription {
    id: string;
    organization: string;
    plan: string;
    status: SubscriptionStatus;
    current_period_start: string;
    current_period_end: string;
    trial_start?: string;
    trial_end?: string;
    canceled_at?: string;
    stripe_subscription_id?: string;
    stripe_customer_id?: string;
    created_at: string;
    updated_at: string;
}

// ============================================================================
// Billing Models (GST Compliance)
// ============================================================================

export type IRASTransactionCode = 'SR' | 'ZR' | 'OS' | 'TX';
export type InvoiceStatus = 'draft' | 'open' | 'paid' | 'void' | 'uncollectible';

export interface Invoice {
    id: string;
    invoice_number: string;
    organization: string;
    organization_name?: string;
    subscription?: string;
    subtotal_cents: number;
    subtotal_dollars?: number;
    gst_rate: number;
    gst_amount_cents: number;
    gst_amount_dollars?: number;
    total_amount_cents: number;
    total_amount_dollars?: number;
    iras_transaction_code: IRASTransactionCode;
    amount_paid_cents: number;
    amount_due_cents?: number;
    currency: 'SGD';
    status: InvoiceStatus;
    paid: boolean;
    due_date: string;
    paid_at?: string;
    pdf_url?: string;
    line_items: Record<string, unknown>[];
    is_overdue?: boolean;
    days_overdue?: number;
    created_at: string;
    updated_at: string;
}

// ============================================================================
// Lead Models
// ============================================================================

export type LeadSource = 'website' | 'demo_request' | 'contact' | 'event' | 'referral' | 'other';
export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'converted' | 'disqualified';

export interface Lead {
    id: string;
    name: string;
    email: string;
    phone?: string;
    company: string;
    job_title?: string;
    source: LeadSource;
    status: LeadStatus;
    notes?: string;
    utm_source?: string;
    utm_medium?: string;
    utm_campaign?: string;
    utm_term?: string;
    utm_content?: string;
    assigned_to?: string;
    assigned_to_email?: string;
    next_follow_up?: string;
    is_converted: boolean;
    converted_at?: string;
    created_at: string;
    updated_at: string;
}

// ============================================================================
// DSAR Models (PDPA Compliance)
// ============================================================================

export type DSARRequestType = 'export' | 'delete' | 'access' | 'rectification';
export type DSARStatus = 'pending' | 'verifying' | 'processing' | 'completed' | 'failed';
export type SLAStatus = 'within_sla' | 'approaching_sla' | 'breached_sla' | 'completed';

export interface DSARRequest {
    id: string;
    user_email: string;
    request_type: DSARRequestType;
    status: DSARStatus;
    sla_status: SLAStatus;
    hours_remaining_in_sla: number;
    is_verified: boolean;
    verified_at?: string;
    requires_approval: boolean;
    is_approved: boolean;
    deletion_approved_at?: string;
    export_url?: string;
    export_expires_at?: string;
    requested_at: string;
    processed_at?: string;
}

// ============================================================================
// API Response Types
// ============================================================================

export interface PaginatedResponse<T> {
    count: number;
    next?: string;
    previous?: string;
    results: T[];
}

export interface ErrorResponse {
    detail?: string;
    error?: string;
    [key: string]: unknown;
}
