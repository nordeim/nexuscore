'use client';

/**
 * Signup Page
 */
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button, Input, Card, CardBody } from '@/components/ui';

export default function SignupPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        company: '',
        password: '',
        confirmPassword: '',
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setIsLoading(true);

        try {
            // TODO: Implement actual signup
            // await api.post('/auth/register/', formData);
            router.push('/verify?email=' + encodeURIComponent(formData.email));
        } catch {
            setError('Failed to create account');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card>
            <CardBody className="p-8">
                <h1 className="text-2xl font-bold text-dark-900 dark:text-white text-center mb-6">
                    Create your account
                </h1>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <Input
                        label="Full Name"
                        name="name"
                        placeholder="John Doe"
                        value={formData.name}
                        onChange={handleChange}
                        required
                    />

                    <Input
                        label="Work Email"
                        name="email"
                        type="email"
                        placeholder="you@company.com"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />

                    <Input
                        label="Company"
                        name="company"
                        placeholder="Company Pte Ltd"
                        value={formData.company}
                        onChange={handleChange}
                        required
                    />

                    <Input
                        label="Password"
                        name="password"
                        type="password"
                        placeholder="••••••••"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />

                    <Input
                        label="Confirm Password"
                        name="confirmPassword"
                        type="password"
                        placeholder="••••••••"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                    />

                    {error && (
                        <p className="text-sm text-red-500 text-center">{error}</p>
                    )}

                    <Button type="submit" fullWidth isLoading={isLoading}>
                        Create Account
                    </Button>
                </form>

                <p className="mt-4 text-xs text-dark-500 text-center">
                    By signing up, you agree to our Terms of Service and Privacy Policy.
                </p>

                <div className="mt-6 text-center text-sm text-dark-500">
                    Already have an account?{' '}
                    <Link href="/login" className="text-singapore-red hover:underline">
                        Sign in
                    </Link>
                </div>
            </CardBody>
        </Card>
    );
}
