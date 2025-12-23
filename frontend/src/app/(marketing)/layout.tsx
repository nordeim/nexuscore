/**
 * Marketing Layout
 * Shared layout for marketing pages with header/footer
 */
import Link from 'next/link';
import { ReactNode } from 'react';

export default function MarketingLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <header className="sticky top-0 z-50 bg-white/80 dark:bg-dark-900/80 backdrop-blur-md border-b border-dark-200 dark:border-dark-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <Link href="/" className="flex items-center gap-2">
                            <span className="text-xl font-bold text-singapore-red">Nexus</span>
                            <span className="text-xl font-bold text-secondary-800 dark:text-white">Core</span>
                        </Link>

                        <nav className="hidden md:flex items-center gap-8">
                            <Link href="/pricing" className="text-dark-600 dark:text-dark-300 hover:text-dark-900 dark:hover:text-white">
                                Pricing
                            </Link>
                            <Link href="/about" className="text-dark-600 dark:text-dark-300 hover:text-dark-900 dark:hover:text-white">
                                About
                            </Link>
                            <Link href="/contact" className="text-dark-600 dark:text-dark-300 hover:text-dark-900 dark:hover:text-white">
                                Contact
                            </Link>
                        </nav>

                        <div className="flex items-center gap-4">
                            <Link href="/login" className="text-dark-600 dark:text-dark-300 hover:text-dark-900 dark:hover:text-white">
                                Log in
                            </Link>
                            <Link
                                href="/signup"
                                className="px-4 py-2 bg-singapore-red text-white rounded-lg hover:bg-primary-600 transition-colors"
                            >
                                Sign up
                            </Link>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1">
                {children}
            </main>

            {/* Footer */}
            <footer className="bg-dark-900 text-dark-400 py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-4 gap-8">
                        <div>
                            <div className="flex items-center gap-2 mb-4">
                                <span className="text-xl font-bold text-singapore-red">Nexus</span>
                                <span className="text-xl font-bold text-white">Core</span>
                            </div>
                            <p className="text-sm">
                                Enterprise SaaS platform built for Singapore businesses.
                            </p>
                        </div>

                        <div>
                            <h4 className="text-white font-semibold mb-4">Product</h4>
                            <ul className="space-y-2 text-sm">
                                <li><Link href="/pricing" className="hover:text-white">Pricing</Link></li>
                                <li><Link href="/about" className="hover:text-white">About</Link></li>
                                <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="text-white font-semibold mb-4">Legal</h4>
                            <ul className="space-y-2 text-sm">
                                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
                                <li><a href="#" className="hover:text-white">Terms of Service</a></li>
                                <li><a href="#" className="hover:text-white">PDPA Compliance</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="text-white font-semibold mb-4">Contact</h4>
                            <ul className="space-y-2 text-sm">
                                <li>hello@nexuscore.sg</li>
                                <li>Singapore</li>
                            </ul>
                        </div>
                    </div>

                    <div className="mt-8 pt-8 border-t border-dark-700 text-sm text-center">
                        © {new Date().getFullYear()} NexusCore. All rights reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
}
