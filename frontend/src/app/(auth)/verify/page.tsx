/**
 * Email Verification Page
 */
import { Card, CardBody } from '@/components/ui';

export default function VerifyPage() {
    return (
        <Card>
            <CardBody className="p-8 text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                </div>

                <h1 className="text-2xl font-bold text-dark-900 dark:text-white mb-2">
                    Check your email
                </h1>

                <p className="text-dark-500 mb-6">
                    We&apos;ve sent a verification link to your email address.
                    Please click the link to verify your account.
                </p>

                <p className="text-sm text-dark-400">
                    Didn&apos;t receive the email?{' '}
                    <button className="text-singapore-red hover:underline">
                        Resend verification email
                    </button>
                </p>
            </CardBody>
        </Card>
    );
}
