/**
 * Auth Layout
 * Shared layout for authentication pages
 */
import Link from 'next/link';
import { ReactNode } from 'react';

export default function AuthLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-dark-100 to-dark-200 dark:from-dark-900 dark:to-dark-800 p-4">
            <div className="w-full max-w-md">
                {/* Logo */}
                <Link href="/" className="flex items-center justify-center gap-2 mb-8">
                    <span className="text-2xl font-bold text-singapore-red">Nexus</span>
                    <span className="text-2xl font-bold text-secondary-800 dark:text-white">Core</span>
                </Link>

                {/* Content */}
                {children}

                {/* Footer */}
                <p className="mt-8 text-center text-sm text-dark-500">
                    © {new Date().getFullYear()} NexusCore. All rights reserved.
                </p>
            </div>
        </div>
    );
}
