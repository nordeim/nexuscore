'use client';

/**
 * Pricing Page
 * Shows pricing tiers with GST note
 */
import { useState } from 'react';
import { PricingCard } from '@/components/marketing';

const plans = [
    {
        name: 'Starter',
        description: 'Perfect for small teams',
        priceMonthly: 49,
        priceYearly: 39,
        features: [
            'Up to 5 team members',
            '1,000 leads/month',
            'Basic analytics',
            'Email support',
            'GST invoicing',
        ],
    },
    {
        name: 'Professional',
        description: 'For growing businesses',
        priceMonthly: 99,
        priceYearly: 79,
        featured: true,
        features: [
            'Up to 20 team members',
            '10,000 leads/month',
            'Advanced analytics',
            'Priority support',
            'GST invoicing + Reports',
            'API access',
        ],
    },
    {
        name: 'Enterprise',
        description: 'For large organizations',
        priceMonthly: 249,
        priceYearly: 199,
        features: [
            'Unlimited team members',
            'Unlimited leads',
            'Custom analytics',
            'Dedicated support',
            'Full PDPA toolkit',
            'Custom integrations',
            'SLA guarantee',
        ],
    },
];

export default function PricingPage() {
    const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly');

    return (
        <div className="py-24 bg-white dark:bg-dark-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h1 className="text-4xl font-bold text-dark-900 dark:text-white mb-4">
                        Simple, Transparent Pricing
                    </h1>
                    <p className="text-lg text-dark-500 mb-8">
                        Choose the plan that&apos;s right for your business.
                    </p>

                    {/* Billing Toggle */}
                    <div className="inline-flex items-center bg-dark-100 dark:bg-dark-800 rounded-lg p-1">
                        <button
                            onClick={() => setBillingPeriod('monthly')}
                            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${billingPeriod === 'monthly'
                                    ? 'bg-white dark:bg-dark-700 text-dark-900 dark:text-white shadow'
                                    : 'text-dark-500 hover:text-dark-700'
                                }`}
                        >
                            Monthly
                        </button>
                        <button
                            onClick={() => setBillingPeriod('yearly')}
                            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${billingPeriod === 'yearly'
                                    ? 'bg-white dark:bg-dark-700 text-dark-900 dark:text-white shadow'
                                    : 'text-dark-500 hover:text-dark-700'
                                }`}
                        >
                            Yearly
                            <span className="ml-1 text-xs text-green-600">Save 20%</span>
                        </button>
                    </div>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {plans.map((plan) => (
                        <PricingCard
                            key={plan.name}
                            {...plan}
                            billingPeriod={billingPeriod}
                        />
                    ))}
                </div>

                <p className="mt-12 text-center text-sm text-dark-500">
                    All prices are in SGD and exclude 9% GST.
                    Custom enterprise pricing available upon request.
                </p>
            </div>
        </div>
    );
}
