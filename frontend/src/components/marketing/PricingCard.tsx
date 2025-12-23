/**
 * PricingCard Component
 * Pricing tier card with GST note
 */
import { Button } from '@/components/ui';

interface PricingCardProps {
    name: string;
    description: string;
    priceMonthly: number;
    priceYearly: number;
    features: string[];
    featured?: boolean;
    billingPeriod: 'monthly' | 'yearly';
}

export function PricingCard({
    name,
    description,
    priceMonthly,
    priceYearly,
    features,
    featured = false,
    billingPeriod,
}: PricingCardProps) {
    const price = billingPeriod === 'monthly' ? priceMonthly : priceYearly;
    const savings = Math.round((1 - priceYearly / priceMonthly) * 100);

    return (
        <div
            className={`
        relative rounded-2xl p-8
        ${featured
                    ? 'bg-singapore-red text-white ring-4 ring-singapore-red/50'
                    : 'bg-white dark:bg-dark-800 border border-dark-200 dark:border-dark-700'
                }
      `}
        >
            {featured && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-secondary-800 text-white text-sm font-medium rounded-full">
                    Most Popular
                </div>
            )}

            <h3 className={`text-xl font-bold ${featured ? 'text-white' : 'text-dark-900 dark:text-white'}`}>
                {name}
            </h3>
            <p className={`mt-2 text-sm ${featured ? 'text-white/80' : 'text-dark-500'}`}>
                {description}
            </p>

            <div className="mt-6">
                <span className={`text-4xl font-bold ${featured ? 'text-white' : 'text-dark-900 dark:text-white'}`}>
                    ${price}
                </span>
                <span className={`text-sm ${featured ? 'text-white/80' : 'text-dark-500'}`}>
                    /month
                </span>
                {billingPeriod === 'yearly' && savings > 0 && (
                    <span className={`ml-2 text-sm font-medium ${featured ? 'text-white' : 'text-green-600'}`}>
                        Save {savings}%
                    </span>
                )}
            </div>

            <p className={`mt-2 text-xs ${featured ? 'text-white/70' : 'text-dark-400'}`}>
                *All prices exclude 9% GST
            </p>

            <ul className="mt-6 space-y-3">
                {features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-2">
                        <svg
                            className={`w-5 h-5 mt-0.5 flex-shrink-0 ${featured ? 'text-white' : 'text-singapore-red'}`}
                            fill="currentColor"
                            viewBox="0 0 20 20"
                        >
                            <path
                                fillRule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clipRule="evenodd"
                            />
                        </svg>
                        <span className={`text-sm ${featured ? 'text-white/90' : 'text-dark-600 dark:text-dark-300'}`}>
                            {feature}
                        </span>
                    </li>
                ))}
            </ul>

            <Button
                variant={featured ? 'secondary' : 'primary'}
                fullWidth
                className="mt-8"
            >
                Get Started
            </Button>
        </div>
    );
}
