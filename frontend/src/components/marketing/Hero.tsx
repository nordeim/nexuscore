/**
 * Hero Component
 * Marketing homepage hero section
 */
import Link from 'next/link';
import { Button } from '@/components/ui';

export function Hero() {
    return (
        <section className="relative overflow-hidden bg-gradient-to-br from-dark-900 via-secondary-900 to-dark-900 py-24 sm:py-32">
            {/* Background decoration */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -top-1/2 -right-1/4 w-96 h-96 bg-singapore-red/20 rounded-full blur-3xl" />
                <div className="absolute -bottom-1/2 -left-1/4 w-96 h-96 bg-secondary-500/20 rounded-full blur-3xl" />
            </div>

            <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center">
                    <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
                        Enterprise SaaS for{' '}
                        <span className="text-singapore-red">Singapore</span>
                    </h1>
                    <p className="text-lg sm:text-xl text-dark-300 max-w-2xl mx-auto mb-8">
                        GST compliant. PDPA ready. Built for Singapore businesses.
                        The all-in-one platform for your enterprise needs.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/signup">
                            <Button size="lg">
                                Start Free Trial
                            </Button>
                        </Link>
                        <Link href="/pricing">
                            <Button variant="outline" size="lg" className="text-white border-white hover:bg-white/10">
                                View Pricing
                            </Button>
                        </Link>
                    </div>
                    <p className="mt-4 text-sm text-dark-400">
                        14-day free trial • No credit card required
                    </p>
                </div>
            </div>
        </section>
    );
}
