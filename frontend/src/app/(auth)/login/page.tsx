'use client';

/**
 * Login Page
 */
import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button, Input, Card, CardBody } from '@/components/ui';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            // TODO: Implement actual login
            // const response = await api.post('/auth/login/', { email, password });
            // setAccessToken(response.access);
            router.push('/dashboard');
        } catch {
            setError('Invalid email or password');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card>
            <CardBody className="p-8">
                <h1 className="text-2xl font-bold text-dark-900 dark:text-white text-center mb-6">
                    Welcome back
                </h1>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <Input
                        label="Email"
                        type="email"
                        placeholder="you@company.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />

                    <Input
                        label="Password"
                        type="password"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    {error && (
                        <p className="text-sm text-red-500 text-center">{error}</p>
                    )}

                    <Button type="submit" fullWidth isLoading={isLoading}>
                        Sign in
                    </Button>
                </form>

                <div className="mt-6 text-center text-sm text-dark-500">
                    Don&apos;t have an account?{' '}
                    <Link href="/signup" className="text-singapore-red hover:underline">
                        Sign up
                    </Link>
                </div>
            </CardBody>
        </Card>
    );
}
